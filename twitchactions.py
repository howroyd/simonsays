#!./.venv/bin/python3
import dataclasses
import random
import time

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
        return twitchAction.tag if command.startswith(twitchAction.command) else None
    elif isinstance(twitchAction.command, list):
        return twitchAction.tag if any(item.startswith(command) for item in twitchAction.command) else None
    else:
        return None


def find_command(twitchActions: TwitchActionList, command: str) -> TwitchAction:
    '''Find the command in the list of twitch actions'''
    for twitchAction in twitchActions:
        tag = check_command(twitchAction, command)
        if tag is not None:
            return twitchAction
    return None


@dataclasses.dataclass
class RuntimeData:
    enabled: bool = True
    cooldown: int = 10.0
    random_chance: int = 100
    last_used: float = 0.0
    keybind: str | None = None

    def set_enabled(self, value: bool) -> None:
        self.enabled = value

    def set_cooldown(self, value: int) -> None:
        self.cooldown = value

    def set_random_chance(self, value: int) -> None:
        self.random_chance = value

    def set_keybind(self, value: str) -> None:
        self.keybind = value

    def use_now(self) -> None:
        '''Use the command now'''
        self.last_used = time.time()

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_ready(self) -> bool:
        return time.time() - self.last_used > self.cooldown

    @property
    def check_random_chance(self) -> bool:
        if 100 == self.random_chance:
            return True

        self.last_used = time.time()
        return random.randint(0, 100) <= self.random_chance

    @property
    def can_use(self) -> bool:
        return self.is_enabled and self.is_ready and self.check_random_chance

    def to_dict(self) -> dict[str, float | int | bool | str | None]:
        '''Convert to a dict'''
        return dataclasses.asdict(self)


TwitchRuntimeDict = dict[str, RuntimeData]


def make_runtime_dict(action_list: TwitchActionList, keybinds: dict[str, str] | None = None) -> TwitchRuntimeDict:
    '''Make a runtime dict from a twitch action list'''
    return {twitchAction.tag: RuntimeData() for twitchAction in action_list}
