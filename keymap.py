import logging

from types import FunctionType
from configparser import ConfigParser
from outputs import KeyboardOutputs, MouseOutputs, LogOutputs, PrintOutputs

FunctionArgTuple = tuple[FunctionType, tuple[str, ...]]
Keymap = dict[str, FunctionArgTuple]

MOUSE_COMMANDS = {
    "lmb": "left",
    "mmb": "middle",
    "rmb": "right"
}

MOUSE_IDENTITY = {
    "right":    (1,  0),
    "left":     (-1, 0),
    "up":       (0,  -1),
    "down":     (0,  1),
}

def make_mouse_keymap(config: ConfigParser) -> Keymap:
    ret = {}

    for k, v in config['mouse.chat.commands'].items():
        args = v.split()

        if args[0] in MOUSE_COMMANDS.keys():
            ret[k] = (MouseOutputs.press_button_for, (MOUSE_COMMANDS[args[0]],))
        elif args[0] in MOUSE_IDENTITY.keys():
            ret[k] = (MouseOutputs.move, tuple(x * int(args[1]) for x in MOUSE_IDENTITY[args[0]]))
        else:
            logging.error(f"Unknown mouse command config {k}: {v}")
            raise ValueError

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
                raise ValueError

    return ret

def make_keymap_entry(config: ConfigParser) -> Keymap:
    return make_mouse_keymap(config) | make_keyboard_keymap(config)

def log_keymap(keymap: Keymap, to_console = False) -> None:
    out_fn = logging.debug
    if to_console:
        out_fn = print

        key_length  = max(len(k) for k in keymap.keys())
        key_padding = 5
        key_space   = key_length + key_padding

        func_length  = max(len(v[0].__qualname__) for v in keymap.values())
        func_padding = 1
        func_space   = func_length + func_padding

        for k, v in keymap.items():
            out_fn(f"{k:{key_space}}: ({v[0].__qualname__:{func_space}}, {v[1]})")
    else:
        for k, v in keymap.items():
            out_fn(f"{k}: {(v[0].__qualname__, v[1])}")

easter_eggs: Keymap = {
    "!dungeon": (PrintOutputs.printer, ("In the dungeon, the dark cold dungeon, the mods will start a mutiny tonight! Ahhhhh wooooo!",)),
    "!caulk": (PrintOutputs.printer, ("Caulk or, less frequently, caulking is a material used to seal joints or seams against leakage in various structures and piping.",)),
    "!cock": (PrintOutputs.printer, ("Hahahaha, why did you say cock?",)),
    "!tiethepoll": (PrintOutputs.printer, ("Kat loves it when chat ties the poll!",)),
    "!sosig": (PrintOutputs.printer, ("Kat is a silly sosig!",)),
}