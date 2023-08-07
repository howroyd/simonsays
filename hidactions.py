#!./.venv/bin/python3
import dataclasses
import enum
from typing import Any, Protocol

import actions
import errorcodes

DEBUG = True


def dummy_run(message: str) -> errorcodes.ErrorSet:
    """Dummy run"""
    if DEBUG:
        print(message)
    return errorcodes.errorset(errorcodes.ErrorCode.OK)


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
class MouseMoveCartesianActionConfig:
    """An action to move the mouse in cartesian coordinates"""
    x: int
    y: int
    device: HidType = HidType.MOUSE_MOVE


class MouseMoveDirectionUnknown(Exception):
    """Unknown mouse move direction"""
    pass


@enum.unique
class MouseMoveDirection(enum.Enum):
    """Mouse move direction"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    def _missing_(self, value: Any) -> Any:
        """Handle missing values"""
        raise self.MouseMoveDirectionUnknown(f"Unknown mouse move direction: {value}")


@dataclasses.dataclass(slots=True)
class MouseMoveDirectionActionConfig:
    """An action to move the mouse in a direction"""
    distance: int
    direction: MouseMoveDirection
    device: HidType = HidType.MOUSE_MOVE


Config = KeyboardActionConfig | MouseButtonActionConfig | MouseMoveCartesianActionConfig | MouseMoveDirectionActionConfig

#####################################################################


@dataclasses.dataclass(slots=True)
class HidAction(actions.Action, Protocol):
    """An action to a Human Interface Device (keyboard, mouse...)"""
    config: Config


@dataclasses.dataclass(slots=True)
class PressButton:
    """Press a mouse button"""
    config: MouseButtonActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Pressing button: {self.config.button}")


@dataclasses.dataclass(slots=True)
class ReleaseButton:
    """Release a mouse button"""
    config: MouseButtonActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Releasing button: {self.config.button}")


@dataclasses.dataclass(slots=True)
class PressReleaseButton:
    """Press and release a button"""
    config: MouseButtonActionConfig
    delay: float = 0.1

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return errorcodes.errorset([
            PressButton(self.config).run(),
            actions.Wait(self.delay).run(),
            ReleaseButton(self.config).run()
        ])


@dataclasses.dataclass(slots=True)
class MoveMouse:
    """Move the mouse"""
    config: MouseMoveCartesianActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Moving mouse to: {self.config.x}, {self.config.y}")


@dataclasses.dataclass(slots=True)
class MoveMouseRelative:
    """Move the mouse relative to its current position"""
    config: MouseMoveCartesianActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Moving mouse (relative) by: {self.config.x}, {self.config.y}")


@dataclasses.dataclass(slots=True)
class MoveMouseRelativeDirection:
    """Move the mouse relative to its current position in a direction"""
    config: MouseMoveDirectionActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Moving mouse (relative direction) by: {self.config.distance} in direction {self.config.direction.value}")


@dataclasses.dataclass(slots=True)
class PressKey:
    """Press a key"""
    config: KeyboardActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Pressing key: {self.config.key}")


@dataclasses.dataclass(slots=True)
class ReleaseKey:
    """Release a key"""
    config: KeyboardActionConfig

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Releasing key: {self.config.key}")


@dataclasses.dataclass(slots=True)
class PressReleaseKey:
    """Press and release a key"""
    config: KeyboardActionConfig
    delay: float = 0.1

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return errorcodes.errorset([
            PressKey(self.config).run(),
            actions.Wait(self.delay).run(),
            ReleaseKey(self.config).run()
        ])
