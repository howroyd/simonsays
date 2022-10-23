import os.path
from configparser import ConfigParser
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConfigKeys:
    logging         = "logging"
    twitch          = "twitch.tv"
    broadcaster     = "broadcaster.commands"
    keyboard        = "keyboard.chat.commands"
    mouse           = "mouse.chat.commands"

    @staticmethod
    def as_dict() -> dict[str, str]:
        objvars = dict(vars(__class__))
        print(objvars)

        keys_to_delete = []

        for k, v in objvars.items():
            if k.startswith("__"):
                keys_to_delete.append(k)
            elif callable(getattr(ConfigKeys(), k)):
                keys_to_delete.append(k)

        for k in keys_to_delete:
            del objvars[k]

        return objvars

def generate_default_config() -> ConfigParser:
    config = ConfigParser(allow_no_value=True)

    config[ConfigKeys.logging] = {
        "; DEBUG, INFO, WARNING, ERROR, CRITICAL": None,
        "DebugLevel": "INFO"
    }
    config[ConfigKeys.twitch] = {
        "TwitchChannelName": "DrGreenGiant"
    }
    config[ConfigKeys.broadcaster] = {
        "; Allows you to start and stop the keyboard and mouse outputs of this programme when in game": None,
        "OutputToggleOnOff": "shift+backspace",
        "StartState": "on",
    }
    config[ConfigKeys.keyboard] = {
        "; Chat commands, comma seperated = key duration(seconds, optional)": None,
        "forward, forwards":            "w   3",
        "back, backward, backwards":    "s   3",
        "left, strafe left":            "a   2",
        "right, strafe right":          "d   2",
        #"fastforward, fastforwards":    "shift+w   3", # TODO, requires with statement to press shift
        #"fastbackward, fastbackwards":  "shift+s   3", # TODO, requires with statement to press shift
        #"fastleft, fast strafe left":   "shift+a   2", # TODO, requires with statement to press shift
        #"fastright, fast strafe right": "shift+d   2", # TODO, requires with statement to press shift
        "journal":                      "j",
        "talk":                         "v   3",
        "flashlight, torch, light":     "t",
        "throw, yeet, drop":            "g",
        "use":                          "f",
        "switch, change, swap":         "q",
        "crouch":                       "c",
        "pickup, grab":                 "e",
    }
    config[ConfigKeys.mouse] = {
        "; Mouse commands, comma seperated = button or direction (lmb, mmb, rmb, up, down, left, right)": None,
        "; distance is how far the mouse will move when looking around, in pixels (I think)": None,
        "lmb":                          "lmb",
        "mmb":                          "mmb",
        "rmb":                          "rmb",
        "look right, turn right":       "right 500",
        "look left, turn left":         "left 500",
        "look up":                      "up 500",
        "look down":                    "down 500",
        "peek right":                   "right 200",
        "peek left":                    "left 200",
        "peek up":                      "up 200",
        "peek down":                    "down 200",
    }

    return config

def make_default(filename: str) -> ConfigParser:
    config = generate_default_config()

    with open(filename, 'w') as configfile:
        config.write(configfile)

    return config

def get_from_file(filename: str = "config.ini") -> ConfigParser:
    if not os.path.isfile(filename):
        make_default(filename)
    cfg = ConfigParser()
    cfg.read(filename)
    return cfg

def print_config(config: ConfigParser) -> None:
    for key in config[ConfigKeys.default]:
        print(f"""{key} is {config[ConfigKeys.default][key]}""")

    for section in config.sections():
        for key in config[section]:
            print(f"""{key} is {config[section][key]}""")

if __name__ == "__main__":
    cfg = get_from_file("default.ini")
    print_config(cfg)