VERSION = 0.2

import logging
from logging.handlers import TimedRotatingFileHandler

import sys, keyboard
from time import sleep
from keymap import easter_eggs
from types import FunctionType
from dataclasses import dataclass
from pathlib import Path

import keyboard, mouse

from configparser import ConfigParser

import twitch, outputs
from default_config import get_from_file, print_config

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
    directory = "logs"
    filename = "log"
    Path(directory).mkdir(parents=True, exist_ok=True)

    h = TimedRotatingFileHandler(
                f"{directory}/{filename}",
                encoding="utf-8",
                when="m",
                interval=1,
                backupCount=10
            )
    h.namer = lambda name: name.replace(".log", "") + ".log"

    logging.root.handlers = []
    logging.basicConfig(
        level=logging.INFO, # Change this to change the global logging level. Normally .INFO, or if needed, .DEBUG
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%y%m%d %H:%M:%S",
        handlers=[
            h,
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
    matches = [value for key, value in key_to_function_map.items() if message.startswith(tuple(key.split(',')))]
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



def make_mouse_keymap(config: ConfigParser):
    mouse_commands = {
        "lmb": "left",
        "mmb": "middle",
        "rmb": "right"
    }

    mouse_movement = {
        "right":    (100, 0),
        "left":     (-100, 0),
        "up":       (0, -100),
        "down":     (0, 100),
    }

    ret = {}

    for k, v in config['mouse.chat.commands'].items():
        args = v.split()

        if args[0] in mouse_commands.keys():
            ret[k] = (outputs.MouseOutputs.press_button_for, (mouse_commands[args[0]],))
        elif args[0] in mouse_movement.keys():
            ret[k] = (outputs.MouseOutputs.move, (*mouse_movement[args[0]],))
        else:
            logging.error(f"Unknown mouse command config {k}: {v}")

    return ret

def make_keyboard_keymap(config: ConfigParser):
    ret = {}

    for k, v in config['keyboard.chat.commands'].items():
        args = v.split()

        match len(args):
            case 1:
                ret[k] = (outputs.KeyboardOutputs.press_key, tuple(args))
            case 2:
                ret[k] = (outputs.KeyboardOutputs.press_key_for, (args[0], float(args[1]))) # TODO this arg parse is a bit shit
            case _:
                logging.error(f"Unknown keyboard command config {k}: {v}")

    return ret

def make_keymap_entry(config: ConfigParser):
    return make_mouse_keymap(config) | make_keyboard_keymap(config)

if __name__ == "__main__":
    config = get_from_file()
    print_config(config)

    channel = config['twitch.tv']['TwitchChannelName']
    start_key = config['broadcaster.commands']['OutputToggleOnOff']

    keymap = make_keymap_entry(config)

    for k, v in keymap.items():
        print(f"{k}: {v}")

    setup_logging()

    print_preamble(start_key)
    is_active = OnOffSwitch()
    onOffHandler = keyboard.add_hotkey(start_key, lambda is_active=is_active: is_active.toggle())

    with twitch.ChannelConnection(channel) as tw:
        logging.info(f"Connected to #{channel}")

        while True:
            tw.run()
            msgs = tw.get_chat_messages()
            for x in msgs:
                channel, message = x.payload_as_tuple()
                logging.debug(f"From {x.username} in {channel}: {message}")

                fn, args = message_filter(message, keymap | easter_eggs)
                if fn and is_active.state:
                    #sleep(1)
                    fn(*args)
            sleep(0.1)