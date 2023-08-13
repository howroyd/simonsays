#!./.venv/bin/python3
import concurrent.futures as cf
import contextlib
import functools
from typing import Callable

import config
import errorcodes
import gui
import offlineirc
import phasmoactions
import twitchactions
import twitchirc

VERSION = "2.0.0"


def done_callback(future: cf.Future, msg: twitchirc.TwitchMessage, tag: str) -> None:
    """Callback for when a command is done"""
    result: errorcodes.ErrorSet = future.result()

    if errorcodes.success(result):
        print(f"Done \'{tag}\' from {msg.username}")
    else:
        print(f"Failed \'{tag}\' from {msg.username} ({result=})")


def make_phasmo_actions(globalconfig: config.Config) -> phasmoactions.ActionDict:
    """Make the phasmo actions"""
    return phasmoactions.all_actions_dict(lambda: phasmoactions.Config({key: item.phasmo for key, item in globalconfig.config.items()}))


def make_random_phasmo_action(globalconfig: config.Config) -> phasmoactions.RandomAction:
    """Make a random phasmo action"""
    return phasmoactions.RandomAction(lambda: phasmoactions.Config({key: item.phasmo for key, item in globalconfig.config.items()}))


def get_twitch_config_fn(globalconfig: config.Config) -> twitchactions.Config:
    """Get the twitch config"""
    return lambda: twitchactions.Config({key: item.twitch for key, item in globalconfig.config.items()})


def make_twitch_actions(globalconfig: config.Config) -> twitchactions.ActionDict:
    """Make the twitch actions"""
    return {key: twitchactions.TwitchAction(get_twitch_config_fn(globalconfig), key, value) for key, value in make_phasmo_actions(globalconfig).items()}


def make_random_twitch_action(globalconfig: config.Config, existingactions: twitchactions.ActionDict) -> tuple[twitchactions.ActionDict, config.ConfigDict]:
    """Make a random twitch action"""
    random_action = make_random_phasmo_action(globalconfig)

    random_config = config.ActionConfig(
        phasmo=phasmoactions.RandomActionConfig(lambda: existingactions),
        twitch=twitchactions.TwitchActionConfig(random_action.name, random_chance=10)
    )

    twitchactiondict = {random_action.name: twitchactions.TwitchAction(get_twitch_config_fn(globalconfig), random_action.name, random_action, force_underlying=True)}
    configdict = {random_action.name: random_config}

    return twitchactiondict, configdict


def make_superuser_actions(globalconfig: config.Config, twitch_actions: twitchactions.ActionDict) -> dict[str, Callable]:
    """Make the superuser actions"""
    superuser_actions = {globalconfig.superuser_prefix + " " + key: functools.partial(value.run, force=True) for key, value in twitch_actions.items()}

    return {
        globalconfig.superuser_prefix + " reload": lambda: print("Reload!"),  # TODO
        globalconfig.superuser_prefix + " reset": lambda: [action.clear_cooldown() for action in twitch_actions.values()],
    } | superuser_actions


def find_tag_by_command_in_actions(twitch_actions: twitchactions.ActionDict, command: str) -> str | None:
    """Find a tag by command"""
    for key, action in twitch_actions.items():
        if action.check_command(command):
            return key
    return None


def make_commands_str(globalconfig: config.Config) -> str:
    """Make a command string to paste into chat"""
    return ", ".join((f"{value.twitch.command[0]}" for value in globalconfig.config.values()))


def preamble(globalconfig: config.Config) -> str:
    """Make the preamble"""
    return f"""\n\t\t--- TwitchPlays v{VERSION} ---\n
\tCreated by DrGreenGiant (Simon Howroyd)

\tThis software is licensed under:
\tGNU GENERAL PUBLIC LICENSE version 2.0 (GPL-2.0)

\tFor more information on this software, visit:
\t\thttps://github.com/howroyd/twitchplays

Valid commands are:\n{make_commands_str(globalconfig)}
\n
    """


def get_action_from_message(actions: twitchactions.ActionDict, globalconfig: config.Config, msg: twitchirc.TwitchMessage) -> tuple[twitchactions.TwitchAction, str] | None:
    """Get the action from a message"""
    tag = find_tag_by_command_in_actions(myactions, msg.payload.lower().removeprefix(myconfig.superuser_prefix))
    sudo: bool = msg.payload.strip().lower().startswith(myconfig.superuser_prefix) and msg.username.strip().lower() in myconfig.superusers

    # NOTE: Idea here is that only bots and sudoers can run "random"
    if not tag:
        if msg.username.strip().lower() in myconfig.bots:
            tag = "random"
            sudo = False
        else:
            return None
    elif tag == "random" and not sudo:
        return None

    if not myconfig.enabled:
        print(f"Commands disabled!  Ignoring \'{tag}\' from {msg.username}")
        return None

    if config.check_blocklist(msg.username, abort=False, silent=True):
        return None

    print(f"Running {'superuser ' if sudo else ''}\'{tag}\' from {msg.username}{' in channel ' + msg.channel if len(myconfig.channel) > 1 else ''}")

    return functools.partial(myactions[tag].run, force=sudo), tag


if __name__ == "__main__":
    myconfig = config.Config.load(VERSION)
    myactions = make_twitch_actions(myconfig)

    randomaction, randomconfig = make_random_twitch_action(myconfig, myactions)
    myactions.update(randomaction)
    myconfig.config.update(randomconfig)

    # mysuperuseractions = make_superuser_actions(myconfig, myactions)
    myconfig.save(backup_old=True)

    print(preamble(myconfig))

    with contextlib.ExitStack() as stack:
        executor = stack.enter_context(cf.ThreadPoolExecutor(max_workers=1))

        irc = None
        if config.OFFLINE:
            irc = stack.enter_context(offlineirc.OfflineIrc(myconfig.channel, username="drgreengiant"))
        else:
            irc = stack.enter_context(twitchirc.TwitchIrc(myconfig.channel))

        print(f"Connected to Twitch channel{'s' if len(myconfig.channel) > 1 else ''}: {', '.join(myconfig.channel)}")
        print(f"Superuser{'s' if len(myconfig.superusers) > 1 else ''}: {', '.join(myconfig.superusers)}")
        print()

        mygui = gui.make_gui(myconfig, myactions)

        while True:
            mygui.update()  # Required otherwise you cant click stuff

            msg = irc.get_message(irc)

            if not msg:
                continue

            config.check_blocklist(myconfig.channel)
            config.check_blocklist(msg.channel)

            if actiontag := get_action_from_message(myactions, myconfig, msg):
                action, tag = actiontag
                executor.submit(action).add_done_callback(functools.partial(done_callback, msg=msg, tag=tag))
