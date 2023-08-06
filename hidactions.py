#!./.venv/bin/python3
import dataclasses
import enum
from typing import Protocol

import actions

DEBUG = False


@enum.unique
class HidType(enum.Enum):
    """The type of HID action"""
    KEYBOARD = enum.auto()
    MOUSE_BUTTON = enum.auto()
    MOUSE_MOVE = enum.auto()


@dataclasses.dataclass(slots=True)
class KeyboardActionConfig:
    """An action to a keyboard"""
    key: str
    device: HidType = HidType.KEYBOARD


@dataclasses.dataclass(slots=True)
class MouseButtonActionConfig:
    """An action to a mouse button"""
    button: str
    device: HidType = HidType.MOUSE_BUTTON


@dataclasses.dataclass(slots=True)
class MouseMoveActionConfig:
    """An action to move the mouse"""
    x: int
    y: int
    device: HidType = HidType.MOUSE_MOVE


Config = KeyboardActionConfig | MouseButtonActionConfig | MouseMoveActionConfig

#####################################################################


@dataclasses.dataclass(slots=True)
class HidAction(actions.Action, Protocol):
    """An action to a Human Interface Device (keyboard, mouse...)"""
    config: Config


@dataclasses.dataclass(slots=True)
class PressButton:
    """Press a mouse button"""
    config: MouseButtonActionConfig

    def run(self) -> None:
        """Run the action"""
        if DEBUG:
            print(f"Pressing button: {self.config.button}")


@dataclasses.dataclass(slots=True)
class ReleaseButton:
    """Release a mouse button"""
    config: MouseButtonActionConfig

    def run(self) -> None:
        """Run the action"""
        if DEBUG:
            print(f"Releasing button: {self.config.button}")


@dataclasses.dataclass(slots=True)
class PressReleaseButton:
    """Press and release a button"""
    config: MouseButtonActionConfig
    delay: float = 0.1

    def run(self) -> None:
        """Run the action"""
        PressButton(self.config.keybind).run()
        actions.Wait(self.delay).run()
        ReleaseButton(self.config.keybind).run()


@dataclasses.dataclass(slots=True)
class MoveMouse:
    """Move the mouse"""
    config: MouseMoveActionConfig

    def run(self) -> None:
        """Run the action"""
        if DEBUG:
            print(f"Moving mouse to: {self.config.x}, {self.config.y}")


@dataclasses.dataclass(slots=True)
class MoveMouseRelative:
    """Move the mouse relative to its current position"""
    config: MouseMoveActionConfig

    def run(self) -> None:
        """Run the action"""
        if DEBUG:
            print(f"Moving mouse (relative) by: {self.config.x}, {self.config.y}")


@dataclasses.dataclass(slots=True)
class PressKey:
    """Press a key"""
    config: KeyboardActionConfig

    def run(self) -> None:
        """Run the action"""
        if DEBUG:
            print(f"Pressing key: {self.config.key}")


@dataclasses.dataclass(slots=True)
class ReleaseKey:
    """Release a key"""
    config: KeyboardActionConfig

    def run(self) -> None:
        """Run the action"""
        if DEBUG:
            print(f"Releasing key: {self.config.key}")


@dataclasses.dataclass(slots=True)
class PressReleaseKey:
    """Press and release a key"""
    config: KeyboardActionConfig
    delay: float = 0.1

    def run(self) -> None:
        """Run the action"""
        PressKey(self.config.key).run()
        actions.Wait(self.delay).run()
        ReleaseKey(self.config.key).run()
