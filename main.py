VERSION = 0.1

import logging
from time import sleep
from keymap import iomap, emotemap
from types import FunctionType

import twitch

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%y%m%d %H:%M:%S")

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
        logging.debug("Instantiating Twitch API connection to %s", channel)
        self.channel = channel
        self.impl = twitch.Twitch()
        self.impl.twitch_connect(self.channel)
        
    def receive(self):
        return self.impl.twitch_receive_messages()

def print_preamble(start_key: str, stop_key: str = None):
    if not stop_key:
        stop_key = start_key
        
    print("\TwitchPlays")
    print("Version", VERSION, "\n")
    
    print("For more info visit:")
    print("https://github.com/howroyd/twitchplays\n")
    
    print("To start press", start_key)
    print("To stop press",  stop_key)
    
    print("\n")

def message_filter(message: str, key_to_function_map: dict[str, tuple[FunctionType, tuple[str, ...]]]) -> tuple[FunctionType, tuple[str, ...]]:
    matches = [value for key, value in key_to_function_map.items() if message.startswith(key)]
    if n_matches := len(matches):
        if n_matches > 1:
            logging.warning("Multiple matches to message \"%s\"\n\t%s", message, [(fn.__qualname__, args) for fn, args in matches])
        return matches[0]
    return (None, None)

if __name__ == "__main__":
    print_preamble(START_KEY, STOP_KEY)    
    
    with twitch.ChannelConnection("katatouille93") as tw:
        while True:
            tw.run()
            msgs = tw.get_chat_messages()
            for x in msgs:
                fn, args = message_filter(x.payload_as_tuple()[1], emotemap)
                if fn:
                    fn(*args)
            sleep(0.1)