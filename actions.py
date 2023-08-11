#!./.venv/bin/python3
import dataclasses
import random
import time
from typing import Protocol

import errorcodes

DEBUG = False


@dataclasses.dataclass(slots=True)
class Action(Protocol):
    """Protocol for actions that can be run"""

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        ...


@dataclasses.dataclass(slots=True)
class ActionRepeat:
    """Repeat an action"""
    action: Action
    times: int

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return errorcodes.errorset([self.action.run() for _ in range(self.times)])


@dataclasses.dataclass(slots=True)
class ActionSequence:
    """Run actions in sequence"""
    actions: list[Action]

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        return errorcodes.errorset([action.run() for action in self.actions])


@dataclasses.dataclass(slots=True)
class Wait:
    """Wait for a duration"""
    duration: float

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        if DEBUG:
            print(f"Waiting for {self.duration} seconds")
        time.sleep(self.duration)
        return errorcodes.errorset(errorcodes.ErrorCode.OK)


@dataclasses.dataclass(slots=True)
class WaitRandom:
    """Wait for a random duration"""
    min_duration: float
    max_duration: float
    wait_time: float = None

    def recalculate_wait_time(self) -> None:
        """Calculate the wait time"""
        self.wait_time = random.uniform(self.min_duration, self.max_duration)

    def __post_init__(self) -> None:
        """Post init"""
        self.recalculate_wait_time()

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        if DEBUG:
            print(f"Waiting for {self.wait_time:.2f} seconds")
        time.sleep(self.wait_time)
        return errorcodes.errorset(errorcodes.ErrorCode.OK)


@dataclasses.dataclass(slots=True)
class ActionRepeatWithWait:
    """Repeat an action with a wait between each repeat"""
    action: Action
    times: int
    wait: Wait | WaitRandom
    recalculate_wait: bool = False  # Recalculate the wait time each time if random

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        ret = []
        for _ in range(self.times):
            ret.append(self.action.run())
            if self.recalculate_wait:
                self.wait.recalculate_wait_time()
            ret.append(self.wait.run())
        return errorcodes.errorset(ret)


ActionDict = dict[str, Action]


if __name__ == "__main__":
    print("Hello World!")

    ActionRepeatWithWait(PressReleaseKey("c"), 3, WaitRandom(0.1, 0.5), recalculate_wait=False).run()
    print()
    ActionRepeatWithWait(PressReleaseKey("c"), 3, WaitRandom(0.1, 0.5), recalculate_wait=True).run()
