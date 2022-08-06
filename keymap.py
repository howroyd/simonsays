from outputs import KeyboardOutputs, MouseOutputs, LogOutputs

iomap = {
    "left": (KeyboardOutputs.press_key, ("leftarrow",)),
    "spin": (KeyboardOutputs.press_key_for, ("leftarrow", 3)),
    "lmb":  (MouseOutputs.press_button_for, ("leftmouse", 1)),
    "rmb":  (MouseOutputs.press_button, ("rightmouse",)),
    "mmb":  (MouseOutputs.press_button, ("middlemouse",)),
}

emotemap = {
    "KEKW":             (LogOutputs.log, ("KEKW",)),
    "Kappa":            (LogOutputs.log, ("Kappa",)),
    
    "eldel3Dirty":      (LogOutputs.log, ("eldel3Dirty",)),
    "eldel3HYPERSS":    (LogOutputs.log, ("eldel3HYPERSS",)),
    "eldel3OMEGAREE":   (LogOutputs.log, ("eldel3OMEGAREE",)),
    "eldel3JAM":        (LogOutputs.log, ("eldel3JAM",)),
    "eldel3EYESS":      (LogOutputs.log, ("eldel3EYESS",)),
    "eldel3KappaSlide": (LogOutputs.log, ("eldel3KappaSlide",)),
    "eldel3LUV":        (LogOutputs.log, ("eldel3LUV",)),
    "eldel3HI":         (LogOutputs.log, ("eldel3HI",)),
    
    "katatoSILLY":      (LogOutputs.log, ("katatoSILLY",)),
    "katatoMURDER":     (LogOutputs.log, ("katatoMURDER",)),
    "katatoBONER":      (LogOutputs.log, ("katatoBONER",)),
    "katatoNORTY2":     (LogOutputs.log, ("katatoNORTY2",)),
    "katatoEGGY":       (LogOutputs.log, ("katatoEGGY",)),
    "katatoWave":       (LogOutputs.log, ("katatoWave",)),
    "katatoLOVE":       (LogOutputs.log, ("katatoLOVE",)),
    "katatoHYPE2":      (LogOutputs.log, ("katatoHYPE2",)),
    "katatoRIOT":       (LogOutputs.log, ("katatoRIOT",)),
    "katatoHUG":        (LogOutputs.log, ("katatoHUG",)),
    "katatoNORTY":      (LogOutputs.log, ("katatoNORTY",)),
    "katatoSOSIG":      (LogOutputs.log, ("katatoSOSIG",)),
    "katatoHAH":        (LogOutputs.log, ("katatoHAH",)),
    
    "veekay1":          (LogOutputs.log, ("Veekay emote!",)),
}