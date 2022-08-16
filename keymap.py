import logging

import keyboard, mouse
from outputs import KeyboardOutputs, MouseOutputs, LogOutputs, PrintOutputs

# Mouse API: https://github.com/boppreh/mouse#api
# Keyboard API: https://pypi.org/project/keyboard/

dungeon = "In the dungeon, the dark cold dungeon, the mods will start a mutiny tonight! Ahhhhh wooooo"

iomap = {
    "strafe left":      (keyboard.press_and_release, ("a",)),
    "strafe right":     (keyboard.press_and_release, ("d",)),
    "forward":          (keyboard.press_and_release, ("w",)),
    "backward":         (keyboard.press_and_release, ("s",)),
    "journal":          (keyboard.press_and_release, ("j",)),
    "talk":             (keyboard.press_and_release, ("v",)),
    "crouch":           (keyboard.press_and_release, ("c",)),
    "use":              (keyboard.press_and_release, ("f",)),

    "lmb":              (mouse.click, ("left",)),
    "rmb":              (mouse.click, ("right",)),
    "mmb":              (mouse.click, ("middle",)),

    "spin":             (KeyboardOutputs.press_key_for, ("leftarrow", 3)),
}

EMOTE_PREFIX = "Parsed an emote! "

emotemap = {
    "KEKW":             (LogOutputs.log, (EMOTE_PREFIX + "KEKW",)),
    "Kappa":            (LogOutputs.log, (EMOTE_PREFIX + "Kappa",)),
    #"eldel3Dirty":      (LogOutputs.log, (EMOTE_PREFIX + "eldel3Dirty",)),
    "eldel3HYPERSS":    (LogOutputs.log, (EMOTE_PREFIX + "eldel3HYPERSS",)),
    "eldel3OMEGAREE":   (LogOutputs.log, (EMOTE_PREFIX + "eldel3OMEGAREE",)),
    "eldel3JAM":        (LogOutputs.log, (EMOTE_PREFIX + "eldel3JAM",)),
    "eldel3EYESS":      (LogOutputs.log, (EMOTE_PREFIX + "eldel3EYESS",)),
    "eldel3KappaSlide": (LogOutputs.log, (EMOTE_PREFIX + "eldel3KappaSlide",)),
    "eldel3LUV":        (LogOutputs.log, (EMOTE_PREFIX + "eldel3LUV",)),
    "eldel3HI":         (LogOutputs.log, (EMOTE_PREFIX + "eldel3HI",)),
    "katatoSILLY":      (LogOutputs.log, (EMOTE_PREFIX + "katatoSILLY", logging.WARN)),
    "katatoMURDER":     (LogOutputs.log, (EMOTE_PREFIX + "katatoMURDER",)),
    "katatoBONER":      (LogOutputs.log, (EMOTE_PREFIX + "katatoBONER",)),
    "katatoNORTY2":     (LogOutputs.log, (EMOTE_PREFIX + "katatoNORTY2",)),
    "katatoEGGY":       (LogOutputs.log, (EMOTE_PREFIX + "katatoEGGY",)),
    "katatoWave":       (LogOutputs.log, (EMOTE_PREFIX + "katatoWave",)),
    "katatoLOVE":       (LogOutputs.log, (EMOTE_PREFIX + "katatoLOVE",)),
    "katatoHYPE2":      (LogOutputs.log, (EMOTE_PREFIX + "katatoHYPE2",)),
    "katatoRIOT":       (LogOutputs.log, (EMOTE_PREFIX + "katatoRIOT" + " Riot time!",)),
    "katatoHUG":        (LogOutputs.log, (EMOTE_PREFIX + "katatoHUG",)),
    "katatoNORTY":      (LogOutputs.log, (EMOTE_PREFIX + "katatoNORTY",)),
    "katatoSOSIG":      (LogOutputs.log, (EMOTE_PREFIX + "katatoSOSIG",)),
    "katatoHAH":        (LogOutputs.log, (EMOTE_PREFIX + "katatoHAH",)),

    "!dungeon":         (LogOutputs.log, (dungeon,)),

    "veekay1":          (LogOutputs.log, ("Veekay emote!",)),

    #"katatoHAH ":        (LogOutputs.log, ("katatoHAH2",)), # multiple matching keys in map (enable to test error handling)
}