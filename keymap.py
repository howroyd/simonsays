import logging

import keyboard, mouse
from outputs import KeyboardOutputs, MouseOutputs, LogOutputs, PrintOutputs

# Mouse API: https://github.com/boppreh/mouse#api
# Keyboard API: https://pypi.org/project/keyboard/

easter_eggs = {
    "!dungeon": (PrintOutputs.printer, ("In the dungeon, the dark cold dungeon, the mods will start a mutiny tonight! Ahhhhh wooooo",)),
}