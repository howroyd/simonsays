#!./.venv/bin/python3
import concurrent.futures as cf
import contextlib
import functools
import pprint
from typing import NoReturn

import requests
import semantic_version
from twitchirc_drgreengiant import offlineirc, twitchirc

from . import config, environment, errorcodes, gui, twitchactions

VERSION = environment.getenv("VERSION", "0.0.0dev")


def done_callback(future: cf.Future, msg: twitchirc.TwitchMessage, tag: str) -> None:
    """Callback for when a command is done"""
    result: errorcodes.ErrorSet = future.result()

    if errorcodes.success(result):
        print(f"Done '{tag}' from {msg.username}")
    else:
        print(f"Failed '{tag}' from {msg.username} ({result=})")


def make_commands_str(myconfig: config.Config) -> str:
    """Make a command string to paste into chat"""
    ret = pprint.pformat([value.twitch.command[0] for value in myconfig.config.values()], compact=True)
    return ret.replace("'", "").replace("[", "").replace("]", "")


def license() -> str:
    """Make the license string"""
    return """\tThis program is free software; you can redistribute it and/or modify
\tit under the terms of the GNU General Public License version 2 as published by
\tthe Free Software Foundation.

\tThis program is distributed in the hope that it will be useful,
\tbut WITHOUT ANY WARRANTY; without even the implied warranty of
\tMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
\tGNU General Public License for more details.

\tYou should have received a copy of the GNU General Public License along
\twith this program; if not, write to the Free Software Foundation, Inc.,
\t51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


def preamble(myconfig: config.Config) -> str:
    """Make the preamble"""
    return f"""\n\t\t---  ---\n
\tSimonSays v{VERSION} - Twitch chat interaction to keyboard and mouse
\tcommands, aimed at Phasmophobia game livestreams.
\tCopyright (C) 2023 Simon Howroyd

{license()}

\tFor more information on this software, visit:
\t\thttps://github.com/howroyd/SimonSays

Valid commands are:
{make_commands_str(myconfig)}

Channels set in config.toml:
{', '.join(myconfig.channel)}

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
        print(f"Commands disabled!  Ignoring '{tag}' from {msg.username}")
        return None

    if config.check_blocklist(msg.username, abort=False, silent=True):
        return None

    print(f"Running {'superuser ' if sudo else ''}'{tag}' from {msg.username}{' in channel ' + msg.channel if len(myconfig.channel) > 1 else ''}")

    return functools.partial(myconfig.actions[tag].run, force=sudo), tag


def check_for_updates() -> semantic_version.Version | None:
    latest = requests.get("https://api.github.com/repos/howroyd/simonsays/releases/latest")
    latestversion = semantic_version.Version(latest.json()["tag_name"].lstrip("v"))
    thisversion = semantic_version.Version.coerce(VERSION.lstrip("v"))
    if latestversion > thisversion:
        return latestversion
    return None


def main() -> NoReturn:
    myconfig = config.Config.load(VERSION)
    myconfig.save(backup_old=True)

    print(preamble(myconfig))

    with contextlib.ExitStack() as stack:
        executor = stack.enter_context(cf.ThreadPoolExecutor(max_workers=1))

        updateavailable = None
        irc = None
        if config.OFFLINE:
            print("OFFLINE MODE")
            irc = stack.enter_context(offlineirc.OfflineIrc(myconfig.channel, username="drgreengiant"))
        else:
            if updateavailable := check_for_updates():
                print(f"Update available!  Current version: {VERSION}, Latest version: {updateavailable}")
                print(f"https://github.com/howroyd/simonsays/releases/tag/{updateavailable}\n\n")
            irc = stack.enter_context(twitchirc.TwitchIrc(myconfig.channel))

        print(channel_connected(myconfig))

        mygui, exit_event, redraw_gui = gui.make_gui(myconfig, updateavailable=updateavailable)

        while True:
            redraw_gui()  # Required otherwise you can't click stuff

            if exit_event.is_set():
                print("GUI closed, exiting...")
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
