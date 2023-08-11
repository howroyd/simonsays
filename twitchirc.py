#!./.venv/bin/python3
import contextlib
import dataclasses
import datetime
import enum
import multiprocessing as mp
import os
import pprint
import queue
import socket
import time
from typing import NoReturn, Protocol, Self

import bufferedsocket

RECORD_FILE = "irc.log"


@enum.unique
class TwitchMessageEnum(enum.Enum):
    """Message types defined by Twitch IRC server"""
    """Ref: https://dev.twitch.tv/docs/irc/example-parser"""
    JOIN = enum.auto()
    PART = enum.auto()
    NOTICE = enum.auto()
    CLEARCHAT = enum.auto()
    HOSTTARGET = enum.auto()
    PRIVMSG = enum.auto()
    PING = enum.auto()
    CAP = enum.auto()
    GLOBALUSERSTATE = enum.auto()
    USERSTATE = enum.auto()
    ROOMSTATE = enum.auto()
    RECONNECT = enum.auto()
    NUMERIC = enum.auto()  # All numerics lumped in here.  Extend if required

    @classmethod
    def match_message_type(cls, string_to_match: str) -> Self | None:
        """Matches the message type to the TwitchMessageEnum"""
        match string_to_match.strip().upper():
            case "JOIN":
                return cls.JOIN
            case "PART":
                return cls.PART
            case "NOTICE":
                return cls.NOTICE
            case "CLEARCHAT":
                return cls.CLEARCHAT
            case "HOSTTARGET":
                return cls.HOSTTARGET
            case "PRIVMSG":
                return cls.PRIVMSG
            case "PING":
                return cls.PING
            case "CAP":
                return cls.CAP
            case "GLOBALUSERSTATE":
                return cls.GLOBALUSERSTATE
            case "USERSTATE":
                return cls.USERSTATE
            case "ROOMSTATE":
                return cls.ROOMSTATE
            case "RECONNECT":
                return cls.RECONNECT
            case "421" | "001" | "002" | "003" | "004" | "353" | "366" | "372" | "375" | "376":
                return cls.NUMERIC
            case _:
                return None


@dataclasses.dataclass(frozen=True, slots=True)
class TwitchMessageProto(Protocol):
    """Protocol for TwitchMessage"""
    username: str
    channel: str
    payload: str


@dataclasses.dataclass(frozen=True, slots=True)
class TwitchMessage:
    """Represents a message from Twitch IRC server"""
    type: TwitchMessageEnum
    username: str
    channel: str
    payload: str

    @classmethod
    def from_irc_message(cls, irc_msg: str) -> Self | None:
        """Creates a TwitchMessage from an IRC message"""
        msg_type = TwitchMessageEnum.match_message_type(irc_msg.split(maxsplit=2)[1])

        if msg_type is None or msg_type == TwitchMessageEnum.NUMERIC:  # TODO should we keep numerics?
            return None

        line_split = irc_msg.split(maxsplit=3)
        idx_of_msg_type = line_split.index(msg_type.name)

        # Remove the username and PRIVMSG from the line
        line = line_split[idx_of_msg_type + 1:]

        if len(line) != 2:
            return None

        return cls(
            type=msg_type,
            username=line_split[0].split("!")[0].lstrip(":"),
            channel=line[0].lstrip("#"),
            payload=line[1].lstrip(":").rstrip("\r\n")
        )


class NoMessageException(Exception):
    """No message received"""
    pass


@dataclasses.dataclass(slots=True)
class IrcSocket:
    address: tuple[str, int] = dataclasses.field(default_factory=lambda: ("irc.chat.twitch.tv", 6667))
    timeout: float = 0.25
    sock: bufferedsocket.BufferedSocket = dataclasses.field(init=False)

    def __post_init__(self):
        self.sock = bufferedsocket.create_connection(self.address, timeout=self.timeout)

    def close(self) -> None:
        """Closes the connection"""
        self.sock.close()

    def read(self) -> str | None:
        """Reads a line from the buffer"""
        b = self.sock.read()
        if b:
            return b.decode('utf-8')
        return None

    def readlines(self) -> list[str]:
        """Reads all lines from the buffer"""
        return [line.decode('utf-8') for line in self.sock.readlines()]

    def write(self, string: str) -> None:
        """Writes a chunk of data to the buffer"""
        self.sock.write(bytes(string, 'utf-8'))


class IrcSocketManaged(IrcSocket):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


@dataclasses.dataclass(slots=True)
class IrcThreadArgs:
    address: tuple[str, int]
    timeout: float
    username: str
    oauth: str
    channel: list[str]
    max_timeout: float = 5.0
    queue: mp.Queue = dataclasses.field(default_factory=mp.Queue)
    event: mp.Event = dataclasses.field(default_factory=mp.Event)


def _twitch_irc_thread(args: IrcThreadArgs) -> NoReturn:
    """Thread for reading from Twitch IRC server"""
    if RECORD_FILE:
        root = os.path.dirname(os.path.realpath(__file__))
        logdir = os.path.join(root, "logs")
        os.makedirs(logdir, exist_ok=True)
        with open("./logs/" + RECORD_FILE, "a") as f:
            f.write(f"Logging in {__file__} at {datetime.datetime.now().isoformat()}\n")

    while True:
        try:
            print("Connecting to Twitch IRC server")

            with IrcSocketManaged(args.address, args.timeout) as irc, open("./logs/" + RECORD_FILE, "a") if RECORD_FILE else contextlib.nullcontext() as record_file:
                irc.write(f'PASS {args.oauth}\r\n')
                irc.write(f'NICK {args.username}\r\n')
                [irc.write(f'JOIN #{channel.strip().lower()}\r\n') for channel in args.channel]

                args.event.set()

                while True:
                    lines = irc.readlines()

                    if record_file:
                        record_file.writelines(lines)

                    for line in lines:
                        if "PING :tmi.twitch.tv" in line:
                            irc.write("PONG :tmi.twitch.tv\r\n")
                        else:
                            args.queue.put(line)

        except (TimeoutError, socket.timeout, socket.error, socket.gaierror, ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Error in Twitch IRC thread: {e}")
            args.event.clear()
            args.timeout = min(args.max_timeout, args.timeout * 2)
            time.sleep(1)


class TwitchIrcConnectionError(Exception):
    """Failed to connect to the Twitch IRC Server"""
    pass


class TwitchIrc:
    def __init__(self, channel: list[str], username: str | None = None, oauth: str | None = None, timeout: float = None):
        self._processdata = IrcThreadArgs(
            address=("irc.chat.twitch.tv", 6667),
            timeout=0.25,
            username=username or "justinfan97339",
            oauth=oauth or "gfdszgfds",
            channel=channel
        )
        self._process: mp.Process | None = None
        self.timeout: float = timeout or 20.0

    @property
    def queue(self) -> mp.Queue:
        """Returns the queue of messages from the IRC server"""
        return self._processdata.queue

    @property
    def connected(self) -> bool:
        """Returns True if the connection is established"""
        return self._processdata.event.is_set()

    def start(self, *, wait_for_connection: bool = True) -> None:
        """Starts the connection to Twitch IRC server"""
        self._process = mp.Process(target=_twitch_irc_thread, args=(self._processdata,))
        self._process.start()

        if wait_for_connection and not self._processdata.event.wait(self.timeout):
            raise TwitchIrcConnectionError(f"Failed to connect to Twitch IRC server after {self.timeout} seconds")

    def stop(self) -> None:
        """Forcibly terminate the connection.  May deadlock anyone waiting on the queue"""
        #  FIXME - This is a bit of a hack.  We should probably send a message to the thread to tell it to stop
        self._process.terminate() if self._process else None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    @staticmethod
    def get_message(irc: Self, *, timeout: float = 0.1) -> TwitchMessage | None:
        msg: TwitchMessage | None = None
        try:
            queue_msg = irc.queue.get(timeout=timeout)
            msg = TwitchMessage.from_irc_message(queue_msg) if queue_msg else None
            if not msg:
                raise NoMessageException
        except (NoMessageException, queue.Empty):
            pass
        return msg


if __name__ == "__main__":
    with TwitchIrc("drgreengiant") as irc:
        while True:
            msg = TwitchMessage.from_irc_message(irc.queue.get())

            if msg:
                pprint.pprint(msg)
