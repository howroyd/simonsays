import logging

from types import FunctionType
from configparser import ConfigParser
from outputs import KeyboardOutputs, MouseOutputs, LogOutputs, PrintOutputs

FunctionArgTuple = tuple[FunctionType, tuple[str, ...]]
Keymap = dict[str, FunctionArgTuple]

def make_mouse_keymap(config: ConfigParser) -> Keymap:
    mouse_commands = {
        "lmb": "left",
        "mmb": "middle",
        "rmb": "right"
    }

    distance = int(config['mouse.movement']['distance'])
    mouse_movement = {
        "right":    (distance, 0),
        "left":     (-distance, 0),
        "up":       (0, -distance),
        "down":     (0, distance),
    }

    ret = {}

    for k, v in config['mouse.chat.commands'].items():
        args = v.split()

        if args[0] in mouse_commands.keys():
            ret[k] = (MouseOutputs.press_button_for, (mouse_commands[args[0]],))
        elif args[0] in mouse_movement.keys():
            ret[k] = (MouseOutputs.move, (*mouse_movement[args[0]],))
        else:
            logging.error(f"Unknown mouse command config {k}: {v}")

    return ret

def make_keyboard_keymap(config: ConfigParser) -> Keymap:
    ret = {}

    for k, v in config['keyboard.chat.commands'].items():
        args = v.split()

        match len(args):
            case 1:
                ret[k] = (KeyboardOutputs.press_key, tuple(args))
            case 2:
                ret[k] = (KeyboardOutputs.press_key_for, (args[0], float(args[1]))) # TODO this arg parse is a bit shit
            case _:
                logging.error(f"Unknown keyboard command config {k}: {v}")

    return ret

def make_keymap_entry(config: ConfigParser) -> Keymap:
    return make_mouse_keymap(config) | make_keyboard_keymap(config)

def log_keymap(keymap: Keymap) -> None:
    for k, v in keymap.items():
        logging.debug(f"{k}: {v}")

easter_eggs: Keymap = {
    "!dungeon": (PrintOutputs.printer, ("In the dungeon, the dark cold dungeon, the mods will start a mutiny tonight! Ahhhhh wooooo",)),
}