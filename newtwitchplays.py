#!./.venv/bin/python3
import concurrent.futures as cf
import dataclasses
import functools
import queue
import random

import phasmoactions
import twitchactions
import twitchirc
import hidactions
import config
import errorcodes

# import config as configsaver
# import gui

VERSION = "2.0.0"
CHANNEL = "drgreengiant"


def done_callback(future, tag):
    """Callback for when a command is done"""
    result: errorcodes.ErrorSet = future.result()

    if errorcodes.success(result):
        print(f"Done: {tag=}")
    else:
        print(f"Failed: {tag=} {result=}")


def make_phasmo_actions(globalconfig: config.Config) -> phasmoactions.ActionDict:
    """Make the phasmo actions"""
    return phasmoactions.all_actions_dict(lambda: phasmoactions.Config({key: item.phasmo for key, item in globalconfig.config.items()}))


def make_twitch_actions(globalconfig: config.Config) -> twitchactions.ActionDict:
    """Make the twitch actions"""
    def get_twitch_config() -> twitchactions.Config:
        """Get the twitch config"""
        return twitchactions.Config({key: item.twitch for key, item in globalconfig.config.items()})
    return {key: twitchactions.TwitchAction(get_twitch_config, key, value) for key, value in make_phasmo_actions(globalconfig).items()}


def find_tag_by_command_in_actions(twitch_actions: twitchactions.ActionDict, command: str) -> str | None:
    """Find a tag by command"""
    for key, action in twitch_actions.items():
        if action.check_command(command):
            return key
    return None


if __name__ == "__main__":
    myconfig = config.make_config(version=VERSION, channel=CHANNEL)
    myactions = make_twitch_actions(myconfig)

    myconfig.config["cycle_items_and_use"].twitch.command = "chaos"
    myconfig.config["drop_all_items"].twitch.command = "yeet"

    myconfig.config["headbang"].twitch.cooldown = 10

    myconfig.save()
    myconfig = config.Config.load()

    with (cf.ThreadPoolExecutor(max_workers=1) as executor,
            twitchirc.TwitchIrc(CHANNEL) as irc):
        print(f"\nTwitchIrc initialized to channel {CHANNEL}\n")

        # mygui = gui.make_gui(runtime)

        # configsaver.save_config(runtime)

        while True:
            msg: twitchirc.TwitchMessage | None = None
            try:
                queue_msg = irc.queue.get(timeout=0.1)
                msg = twitchirc.TwitchMessage.from_irc_message(queue_msg) if queue_msg else None
            except queue.Empty:
                pass
            # mygui.update()

            if not msg:
                continue

            command = msg.payload

            tag = find_tag_by_command_in_actions(myactions, command)

            if tag is not None:
                future = executor.submit(myactions[tag].run)
                future.add_done_callback(functools.partial(done_callback, tag=tag))
