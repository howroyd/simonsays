import os.path
from configparser import ConfigParser

class ConfigKeys:
    default         = "DEFAULT"
    logging         = "logging"
    twitch          = "twitch.tv"
    broadcaster     = "broadcaster.commands"
    keyboard        = "keyboard.chat.commands"
    mouse_config    = "mouse.movement"
    mouse           = "mouse.chat.commands"

def generate_default_config() -> ConfigParser:
    config = ConfigParser(allow_no_value=True)

    config[ConfigKeys.default] = {}
    config[ConfigKeys.logging] = {
        "; DEBUG, INFO, WARNING, ERROR, CRITICAL": None,
        "DebugLevel": "INFO"
    }
    config[ConfigKeys.twitch] = {
        "TwitchChannelName": "katatouille93"
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
        "journal":                      "j",
        "talk":                         "v",
    }
    config[ConfigKeys.mouse_config] = {
        "; Mouse config": None,
        "; distance is how far the mouse will move when looking around, in pixels (I think)": None,
        "distance":                     "500",
    }
    config[ConfigKeys.mouse] = {
        "; Mouse commands, comma seperated = button or direction (lmb, mmb, rmb, up, down, left, right)": None,
        "lmb":                          "lmb",
        "mmb":                          "mmb",
        "rmb":                          "rmb",
        "look right":                   "right",
        "look left":                    "left",
        "look up":                      "up",
        "look down":                    "down",
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