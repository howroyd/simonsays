VERSION = 0.9

import logging
from logging.handlers import TimedRotatingFileHandler

from time           import sleep
from dataclasses    import dataclass
import pathlib

import pynput.keyboard

import twitch
import default_config
import keymap

def setup_logging(log_level: int = logging.INFO) -> None:
    """Setup the global logger"""
    directory = "logs"
    filename = "log"
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    h = TimedRotatingFileHandler(
                f"{directory}/{filename}",
                encoding="utf-8",
                when="m",
                interval=30,
                backupCount=10
            )
    h.namer = lambda name: name.replace(".log", "") + ".log"

    logging.root.handlers = []
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%y%m%d %H:%M:%S",
        handlers=[
            h,
            logging.StreamHandler()
        ]
    )
    sourceFilename = __file__.rsplit('\\', 1)[1]
    logging.log(logging.root.getEffectiveLevel(), f"Logging initialised for {sourceFilename} at level {logging.getLevelName(log_level)}")

def print_preamble(start_key: str, mykeymap: keymap.Keymap) -> None:
    """Function to print programme start text to the console.

    Does not go to the logger therefore doesn't go to the logfile.

    Args:
        start_key (str): key to start outputting HID commands
        stop_key (str, optional): key to stop outputting HID commands. Defaults to None which means same as `start_key`.
    """
    print("\n--- TwitchPlays", VERSION, " ---\n")

    print("For more info visit:")
    print("    https://github.com/howroyd/twitchplays\n")

    print("To exit cleanly press: ctrl + c")
    print("    i.e. the \"ctrl\" button and the \"c\" button on you keyboard at the same time!\n")

    print("To toggle keyboard and mouse interactions on or off, press", start_key)

    print("\n")

    keymap.log_keymap(mykeymap, to_console=True)

    print("\n")

def message_filter(message: str, key_to_function_map: keymap.Keymap) -> keymap.FunctionArgTuple:
    matches = [value for key, value in key_to_function_map.items() if message.startswith(tuple(key.split(',')))]

    if n_matches := len(matches):
        if n_matches > 1:
            logging.warning("Multiple matches to message \"%s\"\n\t%s", message, [(fn.__qualname__, args) for fn, args in matches])
        return matches[0]
    return (None, None)

def main() -> None:
    config = default_config.get_from_file()

    channel   = config[default_config.ConfigKeys.twitch]['TwitchChannelName']
    start_key = config[default_config.ConfigKeys.broadcaster]['OutputToggleOnOff']
    log_level = logging.getLevelName(config[default_config.ConfigKeys.logging]['DebugLevel'])

    setup_logging(log_level)
    mykeymap = keymap.make_keymap_entry(config)
    keymap.log_keymap(mykeymap)

    print_preamble(start_key, mykeymap)

    @dataclass(slots=True)
    class OnOffSwitch:
        state: bool = True

        def toggle(self):
            self.state = not self.state
            logging.info("Turned %s" % ("ON" if self.state else "OFF"))

    is_active    = OnOffSwitch()
    #onOffHandler = keyboard.add_hotkey(start_key, lambda is_active=is_active: is_active.toggle())
    onOffHandler = pynput.keyboard.HotKey(
        pynput.keyboard.HotKey.parse('<shift>+<backspace>'),
        lambda is_active=is_active: is_active.toggle()
        )

    with twitch.ChannelConnection(channel) as tw:
        logging.info(f"Connected to #{channel}")

        with pynput.keyboard.Listener(
                on_press=onOffHandler.press,
                on_release=onOffHandler.release
            ) as l:

            while True:
                tw.run()
                msgs = tw.get_chat_messages()

                for x in msgs:
                    channel, message = x.payload_as_tuple()
                    logging.debug(f"From {x.username} in {channel}: {message}")

                    fn, args = message_filter(message, mykeymap | keymap.easter_eggs)

                    if fn:
                        logging.info(f"{fn.__qualname__} with {(*args,)} by {x.username}: {message}")
                        if is_active.state:
                            logging.debug(f"Calling {fn.__name__}")
                            fn(*args)

                sleep(0.01)

if __name__ == "__main__":
    main()