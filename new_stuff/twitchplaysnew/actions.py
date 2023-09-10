#!./.venv/bin/python3
import dataclasses
import time
from typing import Protocol


@dataclasses.dataclass(frozen=True, slots=True)
class Action(Protocol):
    '''Protocol for actions that can be run'''

    def run(self) -> None:
        '''Run the action'''
        ...


@dataclasses.dataclass(frozen=True, slots=True)
class ActionSequence:
    '''A sequence of actions to run'''
    actions: list[Action]

    def run(self) -> None:
        '''Run the sequence of actions'''
        for action in self.actions:
            action.run()


@dataclasses.dataclass(frozen=True, slots=True)
class Wait:
    '''Wait for a number of seconds'''
    seconds: float

    def run(self) -> None:
        print(f"Waiting {self.seconds} seconds")
        time.sleep(self.seconds)


@dataclasses.dataclass(frozen=True, slots=True)
class PressKey:
    '''Press a key on the keyboard'''
    key: str

    def run(self) -> None:
        print(f"Pressing key {self.key}")


@dataclasses.dataclass(frozen=True, slots=True)
class ReleaseKey:
    '''Release a key on the keyboard'''
    key: str

    def run(self) -> None:
        print(f"Releasing key {self.key}")


@dataclasses.dataclass(frozen=True, slots=True)
class PressButton:
    '''Press a button on the mouse'''
    button: str

    def run(self) -> None:
        print(f"Pressing button {self.button}")


@dataclasses.dataclass(frozen=True, slots=True)
class ReleaseButton:
    '''Release a button on the mouse'''
    button: str

    def run(self) -> None:
        print(f"Releasing button {self.button}")


@dataclasses.dataclass(frozen=True, slots=True)
class MoveMouse:
    '''Move the mouse to a position'''
    x: int
    y: int

    def run(self) -> None:
        print(f"Moving mouse to {self.x}, {self.y}")


@dataclasses.dataclass(frozen=True, slots=True)
class MoveMouseRelative:
    '''Move the mouse relative to the current position'''
    x: int
    y: int

    def run(self) -> None:
        print(f"Moving mouse relative to {self.x}, {self.y}")


@dataclasses.dataclass(frozen=True, slots=True)
class PressReleaseKey:
    '''Press a key, wait (optional), then release the key'''
    key: str
    seconds: float | None = None

    def run(self) -> None:
        PressKey(self.key).run()
        Wait(self.seconds).run() if self.seconds else None
        ReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class PressReleaseButton:
    '''Press a button, wait (optional), then release the button'''
    button: str
    seconds: float | None = None

    def run(self) -> None:
        PressButton(self.button).run()
        Wait(self.seconds).run() if self.seconds else None
        ReleaseButton(self.button).run()


def main() -> None:
    print("Hello World!")
    ActionSequence([
        PressKey("a"),
        PressReleaseKey("b", 2),
        ReleaseKey("a"),
    ]).run()


if __name__ == "__main__":
    main()
