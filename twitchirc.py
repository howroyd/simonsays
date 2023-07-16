#!./.venv/bin/python3
import dataclasses
import enum
import time
from typing import Protocol

import bufferedsocket


@enum.unique
class TwitchMessageEnum(enum.Enum):
    '''Message types defined by Twitch IRC server'''
    '''Ref: https://dev.twitch.tv/docs/irc/example-parser'''
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


@dataclasses.dataclass(frozen=True, slots=True)
class TwitchMessage(Protocol):
    '''Represents a message from Twitch IRC server'''
    type: TwitchMessageEnum
    username: str
    payload: str


@dataclasses.dataclass(slots=True)
class IrcSocket:
    address: str = "irc.chat.twitch.tv"
    port: int = 6667
    timeout: float = 0.25
    sock: bufferedsocket.BufferedSocket = dataclasses.field(init=False)

    def __post_init__(self):
        self.sock = bufferedsocket.create_connection((self.address, self.port), timeout=self.timeout)

    def close(self) -> None:
        '''Closes the connection'''
        self.sock.close()

    def read(self) -> str | None:
        '''Reads a line from the buffer'''
        b = self.sock.read()
        if b:
            return b.decode('utf-8')
        return None

    def readlines(self) -> list[str]:
        '''Reads all lines from the buffer'''
        return [line.decode('utf-8') for line in self.sock.readlines()]

    def write(self, string: str) -> None:
        '''Writes a chunk of data to the buffer'''
        self.sock.write(bytes(string, 'utf-8'))


class IrcSocketManaged(IrcSocket):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == "__main__":
    passmsg = 'PASS asdf\r\nNICK justinfan97339\r\n'
    joinmsg = 'JOIN #drgreengiant\r\n'
    pongmsg = 'PONG :tmi.twitch.tv\r\n'

    with IrcSocketManaged() as irc:
        irc.write(passmsg)
        time.sleep(0.5)
        irc.write(joinmsg)
        while True:
            lines = irc.readlines()
            for line in lines:
                print(line)
            time.sleep(0.5)
            irc.write(pongmsg)
