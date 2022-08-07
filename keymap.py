from outputs import KeyboardOutputs, MouseOutputs, LogOutputs, PrintOutputs

dungeon = "In the dungeon, the dark cold dungeon, the mods will start a mutiny tonight! Ahhhhh wooooo"

iomap = {
    "left": (KeyboardOutputs.press_key, ("leftarrow",)),
    "spin": (KeyboardOutputs.press_key_for, ("leftarrow", 3)),
    "lmb":  (MouseOutputs.press_button_for, ("leftmouse", 1)),
    "rmb":  (MouseOutputs.press_button, ("rightmouse",)),
    "mmb":  (MouseOutputs.press_button, ("middlemouse",)),
}

emotemap = {
    "KEKW":             (PrintOutputs.printer, ("KEKW",)),
    "Kappa":            (PrintOutputs.printer, ("Kappa",)),
    
    "eldel3Dirty":      (PrintOutputs.printer, ("eldel3Dirty",)),
    "eldel3HYPERSS":    (PrintOutputs.printer, ("eldel3HYPERSS",)),
    "eldel3OMEGAREE":   (PrintOutputs.printer, ("eldel3OMEGAREE",)),
    "eldel3JAM":        (PrintOutputs.printer, ("eldel3JAM",)),
    "eldel3EYESS":      (PrintOutputs.printer, ("eldel3EYESS",)),
    "eldel3KappaSlide": (PrintOutputs.printer, ("eldel3KappaSlide",)),
    "eldel3LUV":        (PrintOutputs.printer, ("eldel3LUV",)),
    "eldel3HI":         (PrintOutputs.printer, ("eldel3HI",)),
    
    "katatoSILLY":      (PrintOutputs.printer, ("katatoSILLY",)),
    "katatoMURDER":     (PrintOutputs.printer, ("katatoMURDER",)),
    "katatoBONER":      (PrintOutputs.printer, ("katatoBONER",)),
    "katatoNORTY2":     (PrintOutputs.printer, ("katatoNORTY2",)),
    "katatoEGGY":       (PrintOutputs.printer, ("katatoEGGY",)),
    "katatoWave":       (PrintOutputs.printer, ("katatoWave",)),
    "katatoLOVE":       (PrintOutputs.printer, ("katatoLOVE",)),
    "katatoHYPE2":      (PrintOutputs.printer, ("katatoHYPE2",)),
    "katatoRIOT":       (PrintOutputs.printer, ("Riot time!", "katatoRIOT",)),
    "katatoHUG":        (PrintOutputs.printer, ("katatoHUG",)),
    "katatoNORTY":      (PrintOutputs.printer, ("katatoNORTY",)),
    "katatoSOSIG":      (PrintOutputs.printer, ("katatoSOSIG",)),
    "katatoHAH":        (PrintOutputs.printer, ("katatoHAH",)),
    #"katatoHAH ":        (PrintOutputs.printer, ("katatoHAH2",)), # multiple matching keys in map (enable to test error handling)
    "!dungeon":         (PrintOutputs.printer, (dungeon,)),
    
    "veekay1":          (PrintOutputs.printer, ("Veekay emote!",)),
    
}