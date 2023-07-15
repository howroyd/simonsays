#!./.venv/bin/python3
import dataclasses

import actions


@dataclasses.dataclass(frozen=True, slots=True)
class TwitchAction(actions.Action):
    '''A twitch action'''
    tag: str
    command: str | list[str]


TwitchActionList = list[TwitchAction]


def tag_list(twitchActions: TwitchActionList) -> list[str]:
    '''Get a list of tags'''
    return [twitchAction.tag for twitchAction in twitchActions]


def command_dict(twitchActions: TwitchActionList) -> dict[str, list[str | list[str]]]:
    '''Get a list of commands and tags'''
    return {twitchAction.tag: twitchAction.command for twitchAction in twitchActions}


def check_command(twitchAction: TwitchAction, command: str) -> str | None:
    '''Check if the command matches and return the tag'''
    if isinstance(twitchAction.command, str):
        return twitchAction.tag if command == twitchAction.command else None
    elif isinstance(twitchAction.command, list):
        return twitchAction.tag if command in twitchAction.command else None
    else:
        return None


def find_command(twitchActions: TwitchActionList, command: str) -> TwitchAction:
    '''Find the command in the list of twitch actions'''
    for twitchAction in twitchActions:
        tag = check_command(twitchAction, command)
        if tag is not None:
            return twitchAction
    return None
