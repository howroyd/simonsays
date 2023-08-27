#!./.venv/bin/python3
import concurrent.futures as cf
import contextlib
import functools
from typing import NoReturn

import git
from twitchirc_drgreengiant import offlineirc, twitchirc

from . import config, errorcodes, gui, twitchactions

VERSION = "0.0.0dev"

try:
    VERSION = git.Repo().tags[-1].name
except IndexError:
    # NOTE  When in a GitHub action for pytest, this will fail
    pass


def done_callback(future: cf.Future, msg: twitchirc.TwitchMessage, tag: str) -> None:
    """Callback for when a command is done"""
    result: errorcodes.ErrorSet = future.result()

    if errorcodes.success(result):
        print(f"Done \'{tag}\' from {msg.username}")
    else:
        print(f"Failed \'{tag}\' from {msg.username} ({result=})")


def make_commands_str(myconfig: config.Config) -> str:
    """Make a command string to paste into chat"""
    return ", ".join((f"{value.twitch.command[0]}" for value in myconfig.config.values()))


def preamble(myconfig: config.Config) -> str:
    """Make the preamble"""
    return f"""\n\t\t--- SimonSays v{VERSION} ---\n
\tCreated by twitch.tv/DrGreenGiant (Simon Howroyd)

\tThis software is licensed under:
\tGNU GENERAL PUBLIC LICENSE version 2.0 (GPL-2.0)

\tFor more information on this software, visit:
\t\thttps://github.com/howroyd/SimonSays

Valid commands are:\n{make_commands_str(myconfig)}
\n
    """


def channel_connected(myconfig: config.Config) -> None:
    """Make the text to print when connected to a channel"""
    return f"""Connected to Twitch channel{'s' if len(myconfig.channel) > 1 else ''}: {', '.join(myconfig.channel)}\n
    Superuser{'s' if len(myconfig.superusers) > 1 else ''}: {', '.join(myconfig.superusers)}\n
    """


def get_action_from_message(myconfig: config.Config, msg: twitchirc.TwitchMessage) -> tuple[twitchactions.TwitchAction, str] | None:
    """Get the action from a message"""
    tag = myconfig.find_tag_by_command(msg.payload.lower().removeprefix(myconfig.superuser_prefix))
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

    return functools.partial(myconfig.actions[tag].run, force=sudo), tag


def main() -> NoReturn:
    myconfig = config.Config.load(VERSION)
    myconfig.save(backup_old=True)

    print(preamble(myconfig))

    with contextlib.ExitStack() as stack:
        executor = stack.enter_context(cf.ThreadPoolExecutor(max_workers=1))

        irc = None
        if config.OFFLINE:
            irc = stack.enter_context(offlineirc.OfflineIrc(myconfig.channel, username="drgreengiant"))
        else:
            irc = stack.enter_context(twitchirc.TwitchIrc(myconfig.channel))

        print(channel_connected(myconfig))

        mygui, exit_event = gui.make_gui(myconfig)

        while True:
            mygui.update()  # Required otherwise you cant click stuff
            if exit_event.is_set():
                raise SystemExit

            msg = irc.get_message(irc)

            if not msg:
                continue

            config.check_blocklist(myconfig.channel)
            config.check_blocklist(msg.channel)

            if actiontag := get_action_from_message(myconfig, msg):
                action, tag = actiontag
                executor.submit(action).add_done_callback(functools.partial(done_callback, msg=msg, tag=tag))


if __name__ == "__main__":
    main()
