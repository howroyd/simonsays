#!./.venv/bin/python3
import dataclasses
import random
import time
from typing import Protocol


@dataclasses.dataclass(frozen=True, slots=True)
class Action(Protocol):
    '''Protocol for actions that can be run'''
    def run(self) -> None:
        '''Run the action'''
        ...

@dataclasses.dataclass(frozen=True, slots=True)
class ActionRepeat:
    '''Repeat an action'''
    action: Action
    times: int

    def run(self) -> None:
        '''Run the action'''
        for _ in range(self.times):
            self.action.run()

@dataclasses.dataclass(frozen=True, slots=True)
class ActionSequence:
    '''Run actions in sequence'''
    actions: list[Action]

    def run(self) -> None:
        '''Run the action'''
        for action in self.actions:
            action.run()

@dataclasses.dataclass(frozen=True, slots=True)
class Wait:
    '''Wait for a duration'''
    duration: float

    def run(self) -> None:
        '''Run the action'''
        print(f"Waiting for {self.duration} seconds")
        time.sleep(self.duration)

@dataclasses.dataclass(slots=True)
class WaitRandom:
    '''Wait for a random duration'''
    min_duration: float
    max_duration: float
    wait_time: float = None

    def recalculate_wait_time(self) -> None:
        '''Calculate the wait time'''
        self.wait_time = random.uniform(self.min_duration, self.max_duration)

    def __post_init__(self) -> None:
        '''Post init'''
        self.recalculate_wait_time()

    def run(self) -> None:
        '''Run the action'''
        print(f"Waiting for {self.wait_time:.2f} seconds")
        time.sleep(self.wait_time)

@dataclasses.dataclass(frozen=True, slots=True)
class ActionRepeatWithWait:
    '''Repeat an action with a wait between each repeat'''
    action: Action
    times: int
    wait: Wait | WaitRandom
    recalculate_wait: bool = False  # Recalculate the wait time each time if random

    def run(self) -> None:
        '''Run the action'''
        for _ in range(self.times):
            self.action.run()
            if self.recalculate_wait:
                self.wait.recalculate_wait_time()
            self.wait.run()

###############################################



@dataclasses.dataclass(frozen=True, slots=True)
class PressButton:
    '''Press a button'''
    button: str

    def run(self) -> None:
        '''Run the action'''
        print(f"Pressing button: {self.button}")

@dataclasses.dataclass(frozen=True, slots=True)
class ReleaseButton:
    '''Release a button'''
    button: str

    def run(self) -> None:
        '''Run the action'''
        print(f"Releasing button: {self.button}")

@dataclasses.dataclass(frozen=True, slots=True)
class PressReleaseButton:
    '''Press and release a button'''
    button: str
    delay: float = 0.1

    def run(self) -> None:
        '''Run the action'''
        PressButton(self.button).run()
        Wait(self.delay).run()
        ReleaseButton(self.button).run()

@dataclasses.dataclass(frozen=True, slots=True)
class MoveMouse:
    '''Move the mouse'''
    x: int
    y: int

    def run(self) -> None:
        '''Run the action'''
        print(f"Moving mouse to: {self.x}, {self.y}")

@dataclasses.dataclass(frozen=True, slots=True)
class MoveMouseRelative:
    '''Move the mouse relative to its current position'''
    x: int
    y: int

    def run(self) -> None:
        '''Run the action'''
        print(f"Moving mouse relative: {self.x}, {self.y}")

@dataclasses.dataclass(frozen=True, slots=True)
class PressKey:
    '''Press a key'''
    key: str

    def run(self) -> None:
        '''Run the action'''
        print(f"Pressing key: {self.key}")

@dataclasses.dataclass(frozen=True, slots=True)
class ReleaseKey:
    '''Release a key'''
    key: str

    def run(self) -> None:
        '''Run the action'''
        print(f"Releasing key: {self.key}")

@dataclasses.dataclass(frozen=True, slots=True)
class PressReleaseKey:
    '''Press and release a key'''
    key: str
    delay: float = 0.1

    def run(self) -> None:
        '''Run the action'''
        PressKey(self.key).run()
        Wait(self.delay).run()
        ReleaseKey(self.key).run()



if __name__ == "__main__":
    print("Hello World!")

    ActionRepeatWithWait(PressReleaseKey("c"), 3, WaitRandom(0.1, 0.5), recalculate_wait=False).run()
    print()
    ActionRepeatWithWait(PressReleaseKey("c"), 3, WaitRandom(0.1, 0.5), recalculate_wait=True).run()

