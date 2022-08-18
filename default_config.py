import os.path
from configparser import ConfigParser

def make_default(filename: str) -> ConfigParser:
    config = ConfigParser()

    config['DEFAULT'] = {}
    config['logging'] = {
        "DebugLevel": "DEBUG"
    }
    config['twitch.tv'] = {
        "TwitchChannelName": "katatouille93"
    }
    config['broadcaster.commands'] = {
        "OutputToggleOnOff": "shift+backspace"
    }
    config['keyboard.chat.commands'] = {
        "forward, forwards":            "w   3",
        "back, backward, backwards":    "s   3",
        "left, strafe left":            "a   2",
        "right, strafe right":          "d   2",
        "journal":                      "j",
        "talk":                         "v",
    }
    config['mouse.chat.commands'] = {
        "lmb":                          "lmb",
        "mmb":                          "mmb",
        "rmb":                          "rmb",
        "look right":                   "right",
        "look left":                    "left",
        "look up":                      "up",
        "look down":                    "down",
    }

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
    for key in config["DEFAULT"]:
        print(f"""{key} is {config["DEFAULT"][key]}""")

    for section in config.sections():
        for key in config[section]:
            print(f"""{key} is {config[section][key]}""")

if __name__ == "__main__":
    cfg = get_from_file("default.ini")
    print_config(cfg)