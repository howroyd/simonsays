#!./.venv/bin/python3
import dataclasses
import enum
import platform
from typing import Any, Callable, Protocol, Self

from pynput.keyboard import Controller as Keyboard
from pynput.keyboard import Key, KeyCode
from pynput.keyboard import Listener as KeyboardListener

from . import actions, environment, errorcodes

OPERATINGSYSTEM = platform.platform()
if OPERATINGSYSTEM.startswith("Windows"):
    from pynput.mouse._win32 import Button
    from pynput.mouse._win32 import Controller as Mouse
    from pynput.mouse._win32 import Listener as MouseListener
elif OPERATINGSYSTEM.startswith("Linux"):
    from pynput.mouse._xorg import Button
    from pynput.mouse._xorg import Controller as Mouse
    from pynput.mouse._xorg import Listener as MouseListener
else:
    raise NotImplementedError(f"Unknown platform: {OPERATINGSYSTEM}")


DEBUG = environment.getenvboolean("DEBUG", False)
keyboard = Keyboard()
mouse = Mouse()

keyboard_listener: KeyboardListener | None = None
mouse_listener: MouseListener | None = None

KeybindChangeCallback = Callable[[Key | Button], None]


def start_listeners(on_press: KeybindChangeCallback) -> tuple[KeyboardListener, MouseListener]:
    """Start the listeners for a keyboard or mouse event"""
    global keyboard_listener, mouse_listener

    print("Starting keyboard and mouse listeners...", end="", flush=True)  # NOTE: flushing so it is very clear when we start keylogging

    def on_keyboard(key: Key) -> None:
        """Callback for a keyboard event"""
        on_press(key)

    def on_mouse_button(x, y, button, pressed) -> None:
        """Callback for a mouse event"""
        on_press(button)

    keyboard_listener = KeyboardListener(on_press=on_keyboard)
    keyboard_listener.start()

    mouse_listener = MouseListener(on_click=on_mouse_button)
    mouse_listener.start()

    print("listening", flush=True)

    return (keyboard_listener, mouse_listener)


def stop_listeners() -> None:
    """Stop the keyboard and mouse listeners"""
    global keyboard_listener, mouse_listener

    print("Stopping keyboard and mouse listeners...", end="", flush=True)  # NOTE: flushing so it is very clear when we stop keylogging

    keyboard_listener.stop()
    mouse_listener.stop()

    print("stopped", flush=True)


def dummy_run(message: str) -> errorcodes.ErrorSet:
    """Dummy run"""
    if DEBUG:
        print(message)
    return errorcodes.errorset(errorcodes.ErrorCode.OK)


class ButtonUnknown(Exception):
    """Unknown mouse button"""
    pass


def str_to_button(button: str) -> Button:
    """Convert a string to a pynput mouse button"""
    match button:
        case "left":
            return Button.left
        case "middle":
            return Button.middle
        case "right":
            return Button.right
        case "x1":
            return Button.x1
        case "x2":
            return Button.x2
        case _:
            raise ButtonUnknown(f"Unknown mouse button: {button}")


@enum.unique
class HidType(enum.Enum):
    """The type of HID action"""
    KEYBOARD = enum.auto()  # FIXME remove all autos
    MOUSE_BUTTON = enum.auto()
    MOUSE_MOVE = enum.auto()
    MOUSE_MOVE_DIRECTION = enum.auto()


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


@dataclasses.dataclass(slots=True)
class MouseMoveCartesianSmoothActionConfig:
    """An action to move the mouse in cartesian coordinates in a smooth way"""
    x: int
    y: int
    repeats: int = 10
    pause: float = 0.01
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

    @classmethod
    def _missing_(cls, value: Any) -> Any:
        """Handle missing values"""
        raise MouseMoveDirectionUnknown(f"Unknown mouse move direction: {value}")

    @classmethod
    def to_cartesian(cls, direction: Self | str, distance: int) -> tuple[int, int]:
        """Convert a direction and distance to cartesian coordinates"""
        if isinstance(direction, str):
            direction = cls(direction.strip().lower())
        match direction:
            case cls.UP:
                return (0, -distance)
            case cls.DOWN:
                return (0, distance)
            case cls.LEFT:
                return (-distance, 0)
            case cls.RIGHT:
                return (distance, 0)


@dataclasses.dataclass(slots=True)
class MouseMoveDirectionActionConfig:
    """An action to move the mouse in a direction"""
    distance: int
    direction: MouseMoveDirection
    device: HidType = HidType.MOUSE_MOVE


@dataclasses.dataclass(slots=True)
class MouseMoveDirectionSmoothActionConfig:
    """An action to move the mouse smoothly in a direction"""
    distance: int
    direction: MouseMoveDirection
    repeats: int = 10
    pause: float = 0.01
    device: HidType = HidType.MOUSE_MOVE


Config = KeyboardActionConfig | MouseButtonActionConfig | MouseMoveCartesianActionConfig | MouseMoveCartesianSmoothActionConfig | MouseMoveDirectionActionConfig | MouseMoveDirectionSmoothActionConfig

#####################################################################


@dataclasses.dataclass(slots=True)
class HidAction(actions.Action, Protocol):
    """An action to a Human Interface Device (keyboard, mouse...)"""
    config: Config


@dataclasses.dataclass(slots=True)
class PressButton:
    """Press a mouse button"""
    config: MouseButtonActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            mouse.press(str_to_button(self.config.button))
        return dummy_run(f"Pressing button: {self.config.button}")


@dataclasses.dataclass(slots=True)
class ReleaseButton:
    """Release a mouse button"""
    config: MouseButtonActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            mouse.release(str_to_button(self.config.button))
        return dummy_run(f"Releasing button: {self.config.button}")


@dataclasses.dataclass(slots=True)
class PressReleaseButton:
    """Press and release a button"""
    config: MouseButtonActionConfig
    delay: float = 0.1

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        return errorcodes.errorset([
            PressButton(self.config).run(force=force),
            actions.Wait(self.delay).run(force=force),
            ReleaseButton(self.config).run(force=force)
        ])


@dataclasses.dataclass(slots=True)
class MoveMouse:
    """Move the mouse"""
    config: MouseMoveCartesianActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        return dummy_run(f"Moving mouse to: {self.config.x}, {self.config.y}")


@dataclasses.dataclass(slots=True)
class MoveMouseRelative:
    """Move the mouse relative to its current position"""
    config: MouseMoveCartesianActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            mouse.move(self.config.x, self.config.y)
        return dummy_run(f"Moving mouse (relative) by: {self.config.x}, {self.config.y}")


@dataclasses.dataclass(slots=True)
class MoveMouseRelativeSmooth:
    """Move the mouse relative to its current position"""
    config: MouseMoveCartesianSmoothActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            x = self.config.x // self.config.repeats
            y = self.config.y // self.config.repeats
            look_action = MoveMouseRelative(MouseMoveCartesianActionConfig(x, y))

            return actions.ActionRepeatWithWait(look_action, self.config.repeats, actions.Wait(self.config.pause)).run(force=force)
        return dummy_run(f"Moving mouse smoothly (relative) by: {self.config.x}, {self.config.y} in {self.config.repeats} repeats with {self.config.pause} pause")


@dataclasses.dataclass(slots=True)
class MoveMouseRelativeDirection:
    """Move the mouse relative to its current position in a direction"""
    config: MouseMoveDirectionActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            mouse.move(*MouseMoveDirection.to_cartesian(self.config.direction, self.config.distance))
        return dummy_run(f"Moving mouse (relative direction) by: {self.config.distance} in direction {self.config.direction.value}")


@dataclasses.dataclass(slots=True)
class MoveMouseRelativeDirectionSmooth:
    """Move the mouse relative to its current position, smoothly in a direction"""
    config: MouseMoveDirectionSmoothActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            x, y = MouseMoveDirection.to_cartesian(self.config.direction, self.config.distance)
            x = x // self.config.repeats
            y = y // self.config.repeats
            look_action = MoveMouseRelative(MouseMoveCartesianActionConfig(x, y))

            return actions.ActionRepeatWithWait(look_action, self.config.repeats, actions.Wait(self.config.pause)).run(force=force)
        return dummy_run(f"Moving mouse smoothly (relative direction) by: {self.config.distance} in directino {self.config.direction.value} repeats with {self.config.pause} pause")


@dataclasses.dataclass(slots=True)
class PressKey:
    """Press a key"""
    config: KeyboardActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            if len(self.config.key) > 1:
                keyboard.press(Key[self.config.key])
            else:
                keyboard.press(self.config.key)
        return dummy_run(f"Pressing key: {self.config.key}")


@dataclasses.dataclass(slots=True)
class ReleaseKey:
    """Release a key"""
    config: KeyboardActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if not DEBUG:
            if len(self.config.key) > 1:
                keyboard.release(Key[self.config.key])
            else:
                keyboard.release(self.config.key)
        return dummy_run(f"Releasing key: {self.config.key}")


@dataclasses.dataclass(slots=True)
class PressReleaseKey:
    """Press and release a key"""
    config: KeyboardActionConfig
    delay: float = 0.1

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        return errorcodes.errorset([
            PressKey(self.config).run(force=force),
            actions.Wait(self.delay).run(force=force),
            ReleaseKey(self.config).run(force=force)
        ])

#####################################################################


@dataclasses.dataclass(slots=True)
class PressKeyOrButton:
    """Press a key or button"""
    config: KeyboardActionConfig | MouseButtonActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if isinstance(self.config, KeyboardActionConfig):
            return PressKey(self.config).run(force=force)
        elif isinstance(self.config, MouseButtonActionConfig):
            return PressButton(self.config).run(force=force)
        else:
            raise NotImplementedError(f"Unknown config type: {self.config}")


@dataclasses.dataclass(slots=True)
class ReleaseKeyOrButton:
    """Release a key or button"""
    config: KeyboardActionConfig | MouseButtonActionConfig

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if isinstance(self.config, KeyboardActionConfig):
            return ReleaseKey(self.config).run(force=force)
        elif isinstance(self.config, MouseButtonActionConfig):
            return ReleaseButton(self.config).run(force=force)
        else:
            raise NotImplementedError(f"Unknown config type: {self.config}")


@dataclasses.dataclass(slots=True)
class PressReleaseKeyOrButton:
    """Press and release a key or button"""
    config: KeyboardActionConfig | MouseButtonActionConfig
    delay: float = 0.1

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        if isinstance(self.config, KeyboardActionConfig):
            return PressReleaseKey(self.config, delay=self.delay).run(force=force)
        elif isinstance(self.config, MouseButtonActionConfig):
            return PressReleaseButton(self.config, delay=self.delay).run(force=force)
        else:
            raise NotImplementedError(f"Unknown config type: {self.config}")
