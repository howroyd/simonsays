# DougDoug Note: 
# This is the code that connects to Twitch and checks for new messages.
# You should not need to modify anything in this file, just use as is.
# Original code by Wituz, updated by DDarknut

import sys
import socket
import re
import random
import time
import logging

from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Tuple

from TwitchPlays_KeyCodes import CAPSLOCK

logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%y%m%d %H:%M:%S")
MAX_TIME_TO_WAIT_FOR_LOGIN = 3

@dataclass
class MessageBuilder:
    '''Dataclass to hold a raw incoming bytes and output complete packets defined by the regex pattern'''
    '''Basically a way of assembling partial packets incrementally and knowing when a complete packet has been assembled'''
    parser: re.Pattern[bytes]
    buffer: bytes = b''

    def append(self, new_data: bytes):
        self.buffer += new_data
        
    def clear(self):
        self.buffer = b''
        
    def get_and_clear(self):
        ret = self.buffer
        self.clear()
        return ret

def MessageBuilderDefault() -> MessageBuilder:
    """Default message builder and regex pattern match from the orignal author

    Returns:
        MessageBuilder
    """
    return MessageBuilder(re.compile(b'^(?::(?:([^ !\r\n]+)![^ \r\n]*|[^ \r\n]*) )?([^ \r\n]+)(?: ([^:\r\n]*))?(?: :([^\r\n]*))?\r\n', re.MULTILINE))

@unique
class TwitchMessageEnum(Enum):
    '''Message types defined by Twitch IRC server'''
    '''Ref: https://dev.twitch.tv/docs/irc/example-parser'''
    JOIN            = auto()
    PART            = auto()
    NOTICE          = auto()
    CLEARCHAT       = auto()
    HOSTTARGET      = auto()
    PRIVMSG         = auto()
    PING            = auto()
    CAP             = auto()
    GLOBALUSERSTATE = auto()
    USERSTATE       = auto()
    ROOMSTATE       = auto()
    RECONNECT       = auto()
    NUMERIC         = auto() # All numerics lumped in here.  Extend if required
    
class TwitchIrc:
    '''Definition of the Twitch IRC server'''
    url:  str = "irc.chat.twitch.tv"
    port: int = 6667
    
    @classmethod
    def url_port(cls) -> tuple[str, int]:
        return (cls.url, cls.port)
    
    @staticmethod
    def login_message(username: str, password: str) -> bytes:
        """Make a Twitch IRC login message

        Args:
            username (str): username
            password (str): password (may be a random string if not using authenticated features)

        Returns:
            bytes: bytestring of the login message to be sent to the socket
        """
        return ("PASS %s\r\nNICK %s\r\n" % (password, username)).encode()
    
    @staticmethod
    def join_message(channel: str) -> bytes:
        """Make a Twitch IRC join message to join a channels chat

        Args:
            channel (str): channel name

        Returns:
            bytes: bytestring of the join message to be sent to the socket
        """
        return ("JOIN #%s\r\n" % channel).encode()
    
    @staticmethod
    def pong_message() -> bytes:
        """Make a Twitch IRC pong message reply to a server initiated ping

        Returns:
            bytes: bytestring of the pong message to be sent to the socket
        """
        return b'PONG :tmi.twitch.tv\r\n'
    
    @classmethod
    def split_command_and_packet(cls, packet: bytes) -> tuple[TwitchMessageEnum, bytes]:
        """Take some bytes and try to split them into the command:payload format of the IRC Server

        Args:
            packet (bytes): complete packet in bytes to parse

        Returns:
            tuple[TwitchMessageEnum, bytes]: Tuple of the message type and the rest of the message as bytes
        """
        logging.debug("Splitting: %s", packet)
        ret_fail = (None, None)
        if not packet or 0 == len(packet):
            return ret_fail
        cmd, payload = packet.split(b' ', maxsplit=1)
        if cmd.endswith(b'.tmi.twitch.tv'):
            # Handle stupid case where URL comes first not the command
            cmd, payload = payload.split(b' ', maxsplit=1)

        try:
            return (TwitchMessageEnum[cmd.decode()], payload)
        except KeyError:
            match cmd:
                case ["421" | "001" | "002" | "003" | "004" | "353" | "366" | "372" | "375" | "376"]:
                    return (TwitchMessageEnum.NUMERIC, payload)
                case _:
                    return ret_fail

    @dataclass
    class Message:
        '''Container for a Twitch IRC message'''
        id:      TwitchMessageEnum
        payload: bytes

        @classmethod
        def from_bytes(cls, data: bytes):
            return cls(*TwitchIrc.split_command_and_packet(data))
        
        def payload_as_tuple(self) -> tuple[str, str]:
            channel, message = self.payload.split(b':', maxsplit=1)
            return (channel.decode().rstrip().lstrip('#'), message.decode().lstrip().rstrip())

@dataclass
class TwitchConnection:
    """Create a connection to Twith IRC and login"""
    username:     str           = "justinfan%i" % random.randint(10000, 99999)
    sock:         socket.socket = None
    last_attempt: float         = None # time.time()
    timeout:      float         = 1.0 #1.0 / 60.0
    twitchIrc                   = TwitchIrc()
    
    def is_connected(self) -> bool:
        return True if self.sock else False

    def connect(self) -> bool:
        """Open a socket and send the login message to the Twitch IRC

        Returns:
            bool: true if connected else false or exception
        """
        if not self.is_connected():
            for _ in range(5):
                try:
                    self.last_attempt = time.time()
                    addr = self.twitchIrc.url_port()
                    logging.debug("Creating socket to %s", addr)
                    self.sock = socket.create_connection(addr, self.timeout)
                    break
                except socket.timeout:
                    pass
            
            if not self.is_connected():
                return False
            
            logging.debug("Logging into twitch as %s", self.username)
            self.send(self.twitchIrc.login_message(self.username, "asdf"))
            # todo parse the server response here
        return True
            
    def receive(self, len: int = 4096) -> bytes:
        """Receive any bytes waiting in the socket

        Args:
            len (int, optional): Max number of bytes to get. Defaults to 4096.

        Returns:
            bytes: _description_
        """
        try:
            return self.sock.recv(4096)
        except socket.timeout:
            return None

    def send(self, data: bytes) -> None:
        """Push raw bytes out of the socket

        Args:
            data (bytes): bytes to push
        """
        logging.debug("Sending: %s", data)
        self.sock.send(data)
   
    def disconnect(self):
        if self.is_connected():
            logging.debug("Closing socket to %s", self.twitchIrc.url_port())
            self.sock.close()
        self.sock = None
        
    def reconnect(self) -> bool:
        self.disconnect()
        return self.connect()
    
    def __del__(self): # todo convert to enter and exit dunders so compatible with "with"
        self.disconnect()
        
    def __enter__(self):
        if not self.connect():
            raise socket.timeout
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

class SockHandler:
    '''Wrapper to create the socket and login to twitch on construction'''
    def __init__(self) -> None:
        logging.debug("Init SockHandler")
        self.sock = TwitchConnection()
        if not self.sock.connect():
            raise socket.timeout
    def __del__(self) -> None:
        logging.debug("Deinit SockHandler")
    
class MessageSplitter:
    '''Just to find the start and end of a message and return it'''
    def __call__(self, data: bytes) -> tuple[list[bytes], bytes]: # TODO this is probably redundant??
        packets = data.split(b"\r\n")
        if data.endswith(b"\r\n"):
            return (packets, None)
        else:
            return (packets[:-1], packets[-1])

class BufferedSocket:
    """Container around a Twitch connection, a buffer and a message splitter
    """
    # todo I feel the twitch login should be after this layer, not before
    def __init__(self, splitter: MessageSplitter = None) -> None:
        self.sock     = SockHandler()
        self.buffer   = MessageBuilderDefault()
        self.splitter = splitter if splitter else MessageSplitter()
        
    def receive(self) -> list[bytes]:
        while (buf := self.sock.sock.receive()):
            self.buffer.append(buf)
        full_packets, rest = self.splitter(self.buffer.buffer)
        self.buffer.clear()
        if rest:
            self.buffer.append(rest)
        return full_packets

    def send(self, data: bytes) -> None:
        self.sock.sock.send(data)

class IrcParser:
    def parse(self, packets: list[bytes]) -> list[TwitchIrc.Message]:
        """Take a list of complete packets and parse them into a list of IRC message containers

        Args:
            packets (list[bytes]): list of complete packets in binary

        Returns:
            list[TwitchIrc.Message]: list of IRC messages
        """
        return [TwitchIrc.Message.from_bytes(x) for x in packets if TwitchIrc.Message.from_bytes(x).id is not None]

class IrcConnection:
    """Queue of messages with interface to get more from the socket
    """
    def __init__(self, parser: IrcParser = None, incomingSocket: BufferedSocket = None):
        self.parser = parser if parser else IrcParser()
        self.incomingSocket = incomingSocket if incomingSocket else BufferedSocket()
        self.buf = []
        self.n_max_messages = 50
    
    def get(self, which: TwitchMessageEnum = None) -> list[TwitchIrc.Message]:
        """Get all messages matching an IRC ID and delete them from the internal buffer.

        Args:
            which (TwitchMessageEnum, optional): Which message ID to get.  If None, retrieves them all. Defaults to None.

        Returns:
            list[TwitchIrc.Message]: list of all matching messages received
        """
        if which:
            ret = [x for x in self.buf if x.id == which]
            self.remove_all(which)
            return ret
        else:
            return self.get()
    
    def get_all(self) -> list[TwitchIrc.Message]:
        """Get all messages.  Deletes all contained messages from the internal buffer.

        Returns:
            list[TwitchIrc.Message]: list of all received messages
        """
        ret = self.peek_all()
        self.remove_all()
        return ret
    
    def peek(self, which: TwitchMessageEnum = None) -> list[TwitchIrc.Message]:
        """Get a copy of all messages matching an IRC ID.  Does not delete any messages from the internal buffer.

        Args:
            which (TwitchMessageEnum, optional): Which message ID to get.  If None, retrieves them all. Defaults to None.

        Returns:
            list[TwitchIrc.Message]: list of all matching messages received
        """
        return [x for x in self.peek_all() if x.id == which]
    
    def peek_all(self) -> list[TwitchIrc.Message]:
        """Get a copy of all messages.  Does not delete any messages from the internal buffer.

        Returns:
            list[TwitchIrc.Message]: list of all received messages
        """
        self._get_all()
        return self.buf
    
    def remove_all(self, which: TwitchMessageEnum = None):
        """Delete messages from the internal buffer

        Args:
            which (TwitchMessageEnum, optional): Message ID's to delete, or ALL if None. Defaults to None.
        """
        if which:
            self.buf = [x for x in self.buf if x.id is not which]
        else:
            self.buf = []
    
    def _get_all(self) -> None:
        self.buf += self.parser.parse(self.incomingSocket.receive())
        if len(self.buf) > self.n_max_messages:
            self.buf = self.buf[:-self.n_max_messages] # TODO janky delete the old ones
            logging.debug(self.buf)

class ChannelConnection(IrcConnection):
    """Connection to a Twitch channel's chat
    
    Note; call the run() method periodically so that pingpongs get returned so Twitch doesn't kick us
    """
    def __init__(self, channel: str, parser: IrcParser = None, incomingSocket: BufferedSocket = None):
        super().__init__(parser, incomingSocket)
        self.channel = channel
        self.connected = False;
        
    def run(self):
        if self.peek(TwitchMessageEnum.PING):
            self.incomingSocket.send(TwitchIrc.pong_message())
            self.remove_all(TwitchMessageEnum.PING)
    
    def get_chat_messages(self) -> list[TwitchIrc.Message]:
        return self.get(TwitchMessageEnum.PRIVMSG)
    
    def connect(self) -> bool:
        if self.connected:
            return True

        self.incomingSocket.send(TwitchIrc.join_message(self.channel))
        waitforsecs = 3
        for i in range(waitforsecs):
            for x in self.get_all():
                if x.id == TwitchMessageEnum.JOIN:
                    self.connected = True
                    return True
            time.sleep(0.5)

        raise socket.timeout

    def __enter__(self):
        if not self.connect():
            raise socket.timeout
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

#########################################
### WIP: This is the interface I want ###
#########################################

# with TwitchCLEAN as tw:
#    commands = tw.run(list_of_commands_to_match_against: str)
#    ....do stuff with commands
class TwitchCLEAN:    
    def __init__(self, channel: str):
        self.channel = channel
        self.sock    = SockHandler()
    
    def __enter__(self):
        print("Entering", self.channel)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting", self.channel)
        
    def run(self, matcher: list[str]):
        # Maintain the connection to the *channel*
        # Get any "messages" and filter out matches to arg
        # Return list/queue of matching strings this iter
        pass
