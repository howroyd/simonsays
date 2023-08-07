#!./.venv/bin/python3
import concurrent.futures as cf
import functools
import queue

import config
import errorcodes
import gui
import phasmoactions
import twitchactions
import twitchirc

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


def make_bot_commands(globalconfig: config.Config) -> str:
    """Make a command string to paste into chat"""
    return ", ".join((f"{value.twitch.command}" for value in globalconfig.config.values()))


def preamble(globalconfig: config.Config) -> str:
    """Make the preamble"""
    return f"""\n\t\t--- TwitchPlays v{VERSION} ---\n
\tCreated by DrGreenGiant (Simon Howroyd)

\tThis software is licensed under:
\tGNU GENERAL PUBLIC LICENSE version 2.0 (GPL-2.0)

\tFor more information on this software, visit:
\t\thttps://github.com/howroyd/twitchplays

Valid commands are:\n{make_bot_commands(globalconfig)}
\n\n
    """


if __name__ == "__main__":
    myconfig = config.Config.load(VERSION)
    myactions = make_twitch_actions(myconfig)
    myconfig.save(backup_old=True)

    print(preamble(myconfig))

    with (cf.ThreadPoolExecutor(max_workers=1) as executor,
            twitchirc.TwitchIrc(CHANNEL) as irc):
        print(f"Connected to Twitch channel {CHANNEL}\n")

        mygui = gui.make_gui(myconfig)

        while True:
            mygui.update()  # Required otherwise you cant click stuff

            msg: twitchirc.TwitchMessage | None = None
            try:
                queue_msg = irc.queue.get(timeout=0.1)
                msg = twitchirc.TwitchMessage.from_irc_message(queue_msg) if queue_msg else None
            except queue.Empty:
                pass

            if not msg:
                continue

            tag = find_tag_by_command_in_actions(myactions, msg.payload)

            if not myconfig.enabled:
                print(f"Commands disabled: ignoring \'{tag}\'")
                continue

            if tag is not None:
                future = executor.submit(myactions[tag].run)
                future.add_done_callback(functools.partial(done_callback, tag=tag))
