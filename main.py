VERSION = 0.2

import logging, sys
from logging.handlers import TimedRotatingFileHandler

from time import sleep
from keymap import iomap, emotemap
from types import FunctionType

import twitch

CHANNEL = "katatouille93"
START_KEY: str = "shift+backspace"
STOP_KEY:  str = None # None means use same as START_KEY

test_keys = [
    "lmb",
    "left",
    "spin",
    "bollocks",
    "mmb",
    "rmb",
]

class TwitchAPI:
    def __init__(self, channel: str):
        logging.info("Instantiating Twitch API connection to %s", channel)
        self.channel = channel
        self.impl = twitch.Twitch()
        self.impl.twitch_connect(self.channel)
        
    def receive(self):
        return self.impl.twitch_receive_messages()

def setup_logging() -> None:
    """Setup the global logger
    """
    logging.root.handlers = []
    logging.basicConfig(
        level=logging.DEBUG, # Change this to change the global logging level. Normally .INFO, or if needed, .DEBUG
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%y%m%d %H:%M:%S",
        handlers=[
            TimedRotatingFileHandler(
                "log",
                when="H",
                interval=3,
                backupCount=10
            ),
            #logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )
    logging.log(logging.root.getEffectiveLevel(), "Logging initialised for %s" % __file__.rsplit("\\", 1)[1])

def print_preamble(start_key: str, stop_key: str = None) -> None:
    """Function to print programme start text to the console.
    
    Does not go to the logger therefore doesn't go to the logfile.

    Args:
        start_key (str): key to start outputting HID commands
        stop_key (str, optional): key to stop outputting HID commands. Defaults to None which means same as `start_key`.
    """
    if not stop_key:
        stop_key = start_key
        
    print("\n--- TwitchPlays", VERSION, " ---\n")
    
    print("For more info visit:")
    print("    https://github.com/howroyd/twitchplays\n")
    
    print("To exit cleanly press: ctrl + c")
    print("    i.e. the \"ctrl\" button and the \"c\" button on you keyboard at the same time!\n")
    
    #print("To start press", start_key)
    #print("To stop press",  stop_key)
    
    print("\n")

def message_filter(message: str, key_to_function_map: dict[str, tuple[FunctionType, tuple[str, ...]]]) -> tuple[FunctionType, tuple[str, ...]]:
    """Get the mapped function call for a given message.
    
    This is a glorified keyword based dict lookup.  It will take the first few characters of the message and try to match it to a key.
    It's basically message.startswith(key) where key is from the passed in map.

    Args:
        message (str): text to parse from Twitch chat
        key_to_function_map (dict[str, tuple[FunctionType, tuple[str, ...]]]): map of messages and tuples of function objects with args

    Returns:
        tuple[FunctionType, tuple[str, ...]]: message and function object with args or (None, None)
    """
    matches = [value for key, value in key_to_function_map.items() if message.startswith(key)]
    if n_matches := len(matches):
        if n_matches > 1:
            logging.warning("Multiple matches to message \"%s\"\n\t%s", message, [(fn.__qualname__, args) for fn, args in matches])
        return matches[0]
    return (None, None)

if __name__ == "__main__":
    setup_logging()
    print_preamble(START_KEY, STOP_KEY)    
    
    with twitch.ChannelConnection(CHANNEL) as tw:
        logging.info("Connected to #%s", CHANNEL)
        
        while True:
            tw.run()
            msgs = tw.get_chat_messages()
            for x in msgs:
                logging.info("From: %s: %s" % (x.username, x.payload))
                fn, args = message_filter(x.payload_as_tuple()[1], emotemap | iomap)
                if fn:
                    fn(*args)
            sleep(0.1)