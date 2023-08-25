#!./.venv/bin/python3
import dataclasses
import multiprocessing as mp
import queue
import sys
from typing import NoReturn, Self

from twitchirc_drgreengiant import twitchirc


@dataclasses.dataclass(slots=True)
class OfflineIrcThreadArgs:
    username: str
    channel: list[str]
    queue: mp.Queue = dataclasses.field(default_factory=mp.Queue)


def _offline_irc_thread(args: OfflineIrcThreadArgs) -> NoReturn:
    sys.stdin = open(0)

    while True:
        userinput = sys.stdin.readline().strip()

        msg = twitchirc.TwitchMessage(
            twitchirc.TwitchMessageEnum.PRIVMSG,
            args.username,
            next(iter(args.channel)),
            userinput
        )

        args.queue.put(msg)


class OfflineIrc:
    def __init__(self, channel: list[str], username: str | None = None):
        self._processdata = OfflineIrcThreadArgs(
            username=username or "justinfan97339",
            channel=channel
        )
        self._process: mp.Process | None = None

    @property
    def queue(self) -> mp.Queue:
        """Returns the queue of messages from the IRC server"""
        return self._processdata.queue

    @staticmethod
    def get_message(irc: Self, *, timeout: float = 0.1) -> twitchirc.TwitchMessage | None:
        msg: twitchirc.TwitchMessage | None = None
        try:
            msg = irc.queue.get(timeout=timeout)
            if not msg:
                raise twitchirc.NoMessageException
        except (twitchirc.NoMessageException, queue.Empty):
            pass
        return msg

    def start(self) -> None:
        """Starts the connection to Twitch IRC server"""
        self._process = mp.Process(target=_offline_irc_thread, args=(self._processdata,))
        self._process.start()

    def stop(self) -> None:
        """Forcibly terminate the connection.  May deadlock anyone waiting on the queue"""
        #  FIXME - This is a bit of a hack.  We should probably send a message to the thread to tell it to stop
        self._process.terminate() if self._process else None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
