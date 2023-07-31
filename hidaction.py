#!./.venv/bin/python3
import dataclasses
import random
import time
import enum

import actions


@enum.unique
class HidType(enum.Enum):
    '''The type of HID action'''
    KEYBOARD = enum.auto()
    MOUSE = enum.auto()


@dataclasses.dataclass(slots=True)
class HidAction(actions.Action):
    '''An action to a Human Interface Device (keyboard, mouse...)'''
    HidType: HidType
    enabled: bool = True
    cooldown: int | None = None
    last_used: float = 0.0
    keybind: str | None = None
    random_chance: int | None = None

    def run(self) -> None:
        '''Run the action'''
        if self.random_chance is not None and random.randint(0, 100) > self.random_chance:
            if not super().on_cooldown:
                super().reset_cooldown()
            return
        super().run()

    @property
    def on_cooldown(self) -> bool:
        '''Whether the action is on cooldown'''
        if self.cooldown is None:
            return False
        return time.time() - self.last_used < self.cooldown

    def reset_cooldown(self) -> None:
        '''Reset the cooldown'''
        self.last_used = time.time()

    def run(self) -> None:
        '''Run the action'''
        if not self.enabled:
            return
        if self.on_cooldown:
            return
        if self.random_chance is not None and random.randint(0, 100) > self.random_chance:
            super().reset_cooldown()
            return
        self._run()

    def _run(self) -> None:
        '''Run the action'''
        self.reset_cooldown()
        super().run()
