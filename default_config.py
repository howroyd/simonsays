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
    config = ConfigParser()

    config[ConfigKeys.default] = {}
    config[ConfigKeys.logging] = {
        "DebugLevel": "INFO"
    }
    config[ConfigKeys.twitch] = {
        "TwitchChannelName": "katatouille93"
    }
    config[ConfigKeys.broadcaster] = {
        "OutputToggleOnOff": "shift+backspace"
    }
    config[ConfigKeys.keyboard] = {
        "forward, forwards":            "w   3",
        "back, backward, backwards":    "s   3",
        "left, strafe left":            "a   2",
        "right, strafe right":          "d   2",
        "journal":                      "j",
        "talk":                         "v",
    }
    config[ConfigKeys.mouse_config] = {
        "distance":                     "500",
    }
    config[ConfigKeys.mouse] = {
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
    if os.path.isfile(filename):
        cfg = ConfigParser()
        cfg.read(filename)
        return cfg
    return make_default(filename)

def print_config(config: ConfigParser) -> None:
    for key in config[ConfigKeys.default]:
        print(f"""{key} is {config[ConfigKeys.default][key]}""")

    for section in config.sections():
        for key in config[section]:
            print(f"""{key} is {config[section][key]}""")

if __name__ == "__main__":
    cfg = get_from_file("default.ini")
    print_config(cfg)