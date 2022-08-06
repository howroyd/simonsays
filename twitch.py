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

from TwitchPlays_KeyCodes import CAPSLOCK

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%y%m%d %H:%M:%S")
MAX_TIME_TO_WAIT_FOR_LOGIN = 3

@dataclass
class MessageBuilder:
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
    return MessageBuilder(re.compile(b'^(?::(?:([^ !\r\n]+)![^ \r\n]*|[^ \r\n]*) )?([^ \r\n]+)(?: ([^:\r\n]*))?(?: :([^\r\n]*))?\r\n', re.MULTILINE))

@unique
class TwitchMessageEnum(Enum):
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
    NUMERIC         = auto()

def split_command_and_packet(packet: bytes) -> tuple[TwitchMessageEnum, bytes]:
    logging.debug("Splitting: %s", packet)
    ret_fail = (None, None)
    if not packet or 0 == len(packet):
        return ret_fail
    first, second, third = packet.split(b' ', maxsplit=2) # todo tiudy this. Packet sometimes starts with url not cmd
    if first.endswith(b'.tmi.twitch.tv'):
        first = second
        second = third
    else:
        second = second + third

    try:
        return (TwitchMessageEnum[first.decode()], second)
    except KeyError:
        match first:
            case ["421" | "001" | "002" | "003" | "004" | "353" | "366" | "372" | "375" | "376"]:
                return (TwitchMessageEnum.NUMERIC, second)
            case _:
                return ret_fail

@dataclass
class TwitchMessage:
    id:      TwitchMessageEnum
    payload: bytes

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(*split_command_and_packet(data))




















class TwitchIrc:
    url:  str = "irc.chat.twitch.tv"
    port: int = 6667
    
    @classmethod
    def url_port(cls) -> tuple[str, int]:
        return (cls.url, cls.port)
    
    @staticmethod
    def login_message(username: str, password: str) -> bytes:
        return ("PASS %s\r\nNICK %s\r\n" % (password, username)).encode()
    
    @staticmethod
    def join_message(channel: str) -> bytes:
        return ("JOIN #%s\r\n" % channel).encode()
    
    @staticmethod
    def pong_message() -> bytes:
        return b'PONG :tmi.twitch.tv\r\n'

@dataclass
class TwitchConnection:
    username:     str           = "justinfan%i" % random.randint(10000, 99999)
    sock:         socket.socket = None
    last_attempt: float         = None # time.time()
    timeout:      float         = 1.0 #1.0 / 60.0
    twitchIrc                   = TwitchIrc()
    
    def is_connected(self) -> bool:
        return True if self.sock else False

    def connect(self) -> bool:
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
        
        return True
            
    def receive(self, len: int = 4096) -> bytes:
        try:
            return self.sock.recv(4096)
        except socket.timeout:
            return None

    def send(self, data: bytes) -> None:
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
        #self.sock.connect(('irc.chat.twitch.tv', 6667))
        #self.sock.send(('PASS asdf\r\nNICK %s\r\n' % self.username).encode())
        #self.sock.settimeout(self.timeout)
    
    def __del__(self): # todo convert to enter and exit dunders so compatible with "with"
        self.disconnect()
        
    def __enter__(self):
        if not self.connect():
            raise socket.timeout
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

# @dataclass
# class ChannelConnection:
#     channel: str = None
#     twitch_conn: TwitchConnection = TwitchConnection()
    
#     def connect(self) -> bool:
#         if self.twitch_conn.connect():
#             self.twitctwitch_conn.sock.send(self.twitch.twitchIrc.join_message(self.channel))
#         else:
#             raise socket.timeout

#     def __enter__(self):
#         if not self.connect():
#             raise socket.timeout
    
#     def __exit__(self, exc_type, exc_value, traceback):
#         pass


class SockHandler:
    def __init__(self) -> None:
        print("Init SockHandler")
        self.sock = TwitchConnection()
        if not self.sock.connect():
            raise socket.timeout
    def __del__(self) -> None:
        print("Deinit SockHandler")
    
class MessageSplitter:
    # Just to find the start and end of a message and return it
    def __call__(self, data: bytes) -> tuple[list[bytes], bytes]:
        packets = data.split(b"\r\n")
        if data.endswith(b"\r\n"):
            return (packets, None)
        else:
            return (packets[:-1], packets[-1])

class BufferedSocket:
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
    def parse(self, packets: list[bytes]) -> list[TwitchMessage]:
        return [TwitchMessage.from_bytes(x) for x in packets if TwitchMessage.from_bytes(x).id is not None]

class IrcConnection:
    def __init__(self, parser: IrcParser = None, incomingSocket: BufferedSocket = None):
        self.parser = parser if parser else IrcParser()
        self.incomingSocket = incomingSocket if incomingSocket else BufferedSocket()
        self.buf = []
        self.n_max_messages = 50
    
    def get(self, which: TwitchMessageEnum = None) -> list[TwitchMessage]:
        ret = [x for x in self.get_all() if x.id == which]
        return ret
    
    def get_all(self) -> list[TwitchMessage]:
        ret = self.peek_all()
        self.buf = []
        return ret
    
    def peek(self, which: TwitchMessageEnum = None) -> list[TwitchMessage]:
        return [x for x in self.peek_all() if x.id == which]
    
    def peek_all(self) -> list[TwitchMessage]:
        self._get_all()
        return self.buf
    
    def remove_all(self, which: TwitchMessageEnum):
        self.buf = [x for x in self.buf if x.id is not which]
    
    def _get_all(self) -> None:
        self.buf += self.parser.parse(self.incomingSocket.receive())
        if len(self.buf) > self.n_max_messages:
            self.buf = self.buf[:-self.n_max_messages] # TODO janky delete the old ones
            logging.debug(self.buf)

class ChannelConnection(IrcConnection):
    def __init__(self, channel: str, parser: IrcParser = None, incomingSocket: BufferedSocket = None):
        super().__init__(parser, incomingSocket)
        self.channel = channel
        self.connected = False;
        
    def run(self):
        if self.peek(TwitchMessageEnum.PING):
            self.incomingSocket.send(TwitchIrc.pong_message())
            self.remove_all(TwitchMessageEnum.PING)
    
    def get_chat_messages(self) -> list[str]:
        return []
    
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

# @dataclass
# class ChannelConnection:
#     channel: str = None
#     twitch_conn: TwitchConnection = TwitchConnection()
    
#     def connect(self) -> bool:
#         if self.twitch_conn.connect():
#             self.twitctwitch_conn.sock.send(self.twitch.twitchIrc.join_message(self.channel))
#         else:
#             raise socket.timeout

#     def __enter__(self):
#         if not self.connect():
#             raise socket.timeout
    
#     def __exit__(self, exc_type, exc_value, traceback):
#         pass

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







#####################
### ORIGINAL CODE ###
#####################
class Twitch:
    re_prog = None
    sock = None
    partial = b''
    login_ok = False
    channel = ''
    login_timestamp = 0

    def twitch_connect(self, channel):
        if self.sock:
            self.sock.close()
        
        self.sock = None
        self.partial = b''
        self.login_ok = False
        self.channel = channel

        # Compile regular expression
        self.re_prog = re.compile(b'^(?::(?:([^ !\r\n]+)![^ \r\n]*|[^ \r\n]*) )?([^ \r\n]+)(?: ([^:\r\n]*))?(?: :([^\r\n]*))?\r\n', re.MULTILINE)

        # Create socket
        logging.debug("Connecting to Twitch")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to connect socket
        self.sock.connect(('irc.chat.twitch.tv', 6667))

        # Log in anonymously
        user = 'justinfan%i' % random.randint(10000, 99999)
        logging.debug("Connected to Twitch. Logging in anonymously")
        self.sock.send(('PASS asdf\r\nNICK %s\r\n' % user).encode())

        self.sock.settimeout(1.0/60.0)

        self.login_timestamp = time.time()

    # Attempt to reconnect after a delay
    def reconnect(self, delay):
        time.sleep(delay)
        self.twitch_connect(self.channel)

    # Returns a list of irc messages received
    def receive_and_parse_data(self):
        buffer = b''
        while True:
            received = b''
            try:
                received = self.sock.recv(4096)
            except socket.timeout:
                break
            # except OSError as e:
            #     if e.winerror == 10035:
            #         # This "error" is expected -- we receive it if timeout is set to zero, and there is no data to read on the socket.
            #         break
            except Exception as e:
                logging.error("Unexpected connection error. Will retry. %s", e)
                self.reconnect(1)
                return []
            if not received:
                logging.warning("Connection closed by Twitch. Reconnecting in 5 seconds")
                self.reconnect(5)
                return []
            buffer += received

        if buffer:
            # Prepend unparsed data from previous iterations
            if self.partial:
                buffer = self.partial + buffer
                self.partial = []

            # Parse irc messages
            res = []
            matches = list(self.re_prog.finditer(buffer))
            for match in matches:
                res.append({
                    'name':     (match.group(1) or b'').decode(errors='replace'),
                    'command':  (match.group(2) or b'').decode(errors='replace'),
                    'params':   list(map(lambda p: p.decode(errors='replace'), (match.group(3) or b'').split(b' '))),
                    'trailing': (match.group(4) or b'').decode(errors='replace'),
                })

            # Save any data we couldn't parse for the next iteration
            if not matches:
                self.partial += buffer
            else:
                end = matches[-1].end()
                if end < len(buffer):
                    self.partial = buffer[end:]

                if matches[0].start() != 0:
                    # If we get here, we might have missed a message. pepeW
                    # ⣿⣿⣿⣿⣿⣿⣿⠿⢛⢛⡛⡻⢿⣿⣿⣿⣿⠟⠛⢛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿
                    # ⣿⣿⣿⣿⢟⢱⡔⡝⣜⣜⢜⢜⡲⡬⡉⢕⢆⢏⢎⢇⢇⣧⡉⠿⣿⣿⣿⣿⣿⣿
                    # ⣿⣿⡟⡱⣸⠸⢝⢅⢆⢖⣜⣲⣵⣴⣱⣈⡣⣋⢣⠭⣢⣒⣬⣕⣄⣝⡻⢿⣿⣿
                    # ⣿⠟⡜⣎⢎⢇⢇⣵⣷⣿⣿⡿⠛⠉⠉⠛⢿⣦⢵⣷⣿⣿⣿⠟⠛⠋⠓⢲⡝⣿
                    # ⢏⢰⢱⣞⢜⢵⣿⣿⣿⣿⣿⠁⠐⠄⠄⠄⠄⢹⣻⣿⣿⣿⠡⠄⠄⠄⠄⠄⠹⣺
                    # ⢕⢜⢕⢕⢵⠹⢿⣿⣿⣿⣿⡀⠸⠗⣀⠄⠄⣼⣻⣿⣿⣿⡀⢾⠆⣀⠄⠄⣰⢳
                    # ⡕⣝⢜⡕⣕⢝⣜⢙⢿⣿⣿⣷⣦⣤⣥⣤⣾⢟⠸⢿⣿⣿⣿⣦⣄⣉⣤⡴⢫⣾
                    # ⡪⡪⣪⢪⢎⢮⢪⡪⡲⢬⢩⢩⢩⠩⢍⡪⢔⢆⢏⡒⠮⠭⡙⡙⠭⢝⣨⣶⣿⣿
                    # ⡪⡪⡎⡮⡪⡎⡮⡪⣪⢣⢳⢱⢪⢝⢜⢜⢕⢝⢜⢎⢧⢸⢱⡹⡍⡆⢿⣿⣿⣿
                    # ⡪⡺⡸⡪⡺⣸⠪⠚⡘⠊⠓⠕⢧⢳⢹⡸⣱⢹⡸⡱⡱⡕⡵⡱⡕⣝⠜⢿⣿⣿
                    # ⡪⡺⡸⡪⡺⢐⢪⢑⢈⢁⢋⢊⠆⠲⠰⠬⡨⡡⣁⣉⠨⡈⡌⢥⢱⠐⢕⣼⣿⣿
                    # ⡪⣪⢣⢫⠪⢢⢅⢥⢡⢅⢅⣑⡨⡑⠅⠕⠔⠔⠄⠤⢨⠠⡰⠠⡂⣎⣼⣿⣿⣿
                    # ⠪⣪⡪⡣⡫⡢⡣⡣⡣⡣⡣⣣⢪⡪⡣⡣⡲⣑⡒⡎⡖⢒⣢⣥⣶⣿⣿⣿⣿⣿
                    # ⢁⢂⠲⠬⠩⣁⣙⢊⡓⠝⠎⠮⠮⠚⢎⡣⡳⠕⡉⣬⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
                    # ⢐⠐⢌⠐⠅⡂⠄⠄⢌⢉⠩⠡⡉⠍⠄⢄⠢⡁⡢⠠⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
                    print('either ddarknut fucked up or twitch is bonkers, or both I mean who really knows anything at this point')

            return res

        return []

    def twitch_receive_messages(self):
        privmsgs = []
        for irc_message in self.receive_and_parse_data():
            cmd = irc_message['command']
            if cmd == 'PRIVMSG':
                privmsgs.append({
                    'username': irc_message['name'],
                    'message': irc_message['trailing'],
                })
            elif cmd == 'PING':
                self.sock.send(b'PONG :tmi.twitch.tv\r\n')
            elif cmd == '001':
                print('Successfully logged in. Joining channel %s.' % self.channel)
                self.sock.send(('JOIN #%s\r\n' % self.channel).encode())
                self.login_ok = True
            elif cmd == 'JOIN':
                print('Successfully joined channel %s' % irc_message['params'][0])
            elif cmd == 'NOTICE':
                print('Server notice:', irc_message['params'], irc_message['trailing'])
            elif cmd == '002': continue
            elif cmd == '003': continue
            elif cmd == '004': continue
            elif cmd == '375': continue
            elif cmd == '372': continue
            elif cmd == '376': continue
            elif cmd == '353': continue
            elif cmd == '366': continue
            else:
                print('Unhandled irc message:', irc_message)

        if not self.login_ok:
            # We are still waiting for the initial login message. If we've waited longer than we should, try to reconnect.
            if time.time() - self.login_timestamp > MAX_TIME_TO_WAIT_FOR_LOGIN:
                print('No response from Twitch. Reconnecting...')
                self.reconnect(0)
                return []

        return privmsgs
