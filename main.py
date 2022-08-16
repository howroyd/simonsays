VERSION = 0.2

import logging
from logging.handlers import TimedRotatingFileHandler

import sys, keyboard
from time import sleep
from keymap import iomap, emotemap
from types import FunctionType
from dataclasses import dataclass

import keyboard, mouse

from configparser import ConfigParser

import twitch

CHANNEL   = "katatouille93"
START_KEY = "shift+backspace"

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
        level=logging.INFO, # Change this to change the global logging level. Normally .INFO, or if needed, .DEBUG
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%y%m%d %H:%M:%S",
        handlers=[
            TimedRotatingFileHandler(
                "log",
                encoding="utf-8",
                when="H",
                interval=3,
                backupCount=10
            ),
            #logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )
    logging.log(logging.root.getEffectiveLevel(), "Logging initialised for %s" % __file__.rsplit("\\", 1)[1])

def print_preamble(start_key: str) -> None:
    """Function to print programme start text to the console.

    Does not go to the logger therefore doesn't go to the logfile.

    Args:
        start_key (str): key to start outputting HID commands
        stop_key (str, optional): key to stop outputting HID commands. Defaults to None which means same as `start_key`.
    """
    print("\n--- TwitchPlays", VERSION, " ---\n")

    print("For more info visit:")
    print("    https://github.com/howroyd/twitchplays\n")

    print("To exit cleanly press: ctrl + c")
    print("    i.e. the \"ctrl\" button and the \"c\" button on you keyboard at the same time!\n")

    print("To toggle keyboard and mouse interactions on or off, press", start_key)

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

@dataclass
class OnOffSwitch:
    state: bool = True

    def toggle(self):
        self.state = not self.state
        logging.info("Turned %s" % ("ON" if self.state else "OFF"))




def get_config_chat_commands(config: ConfigParser):
    return config["chat.commands"]

def make_keymap_entry(config: ConfigParser):
    mouse_commands = {
        "lmb": "left",
        "mmb": "middle",
        "rmb": "right"
    }

    ret = {}

    for key in get_config_chat_commands(config):
        value = config["chat.commands"][key]

        match value.split()[0]:
            case [mouse_commands.keys()]:
                ret[key] = (mouse.click, (mouse_commands[value],))
            case _:
                ret[key] = (keyboard.press_and_release, tuple(value.split()))

    return ret

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")
    for key in config["DEFAULT"]:
        print(f"""{key} is {config["DEFAULT"][key]}""")
    for section in config.sections():
        for key in config[section]:
            print(f"""{key} is {config[section][key]}""")


    print(make_keymap_entry(config))

    setup_logging()

    print_preamble(START_KEY)
    is_active = OnOffSwitch()
    onOffHandler = keyboard.add_hotkey(START_KEY, lambda is_active=is_active: is_active.toggle())

    with twitch.ChannelConnection(CHANNEL) as tw:
        logging.info("Connected to #%s", CHANNEL)

        while True:
            tw.run()
            msgs = tw.get_chat_messages()
            for x in msgs:
                channel, message = x.payload_as_tuple()
                logging.debug(f"From {x.username} in {channel}: {message}")

                fn, args = message_filter(message, emotemap | iomap)
                if fn and is_active.state:
                    #sleep(1)
                    fn(*args)
            sleep(0.1)