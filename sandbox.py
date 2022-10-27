from time import sleep, time
from tkinter import W
from typing import Any, Optional, Callable
import multiprocessing as mp
import concurrent.futures
from threading import Thread
from dataclasses import dataclass, field
import random

from pyparsing import Forward
@dataclass
class Command:
    keys: list[str]
    fn: Callable
    args: list = field(default_factory=list)
    last_run: float = 0
    is_running: bool = False
    random_chance: int = 50
    cooldown: float = 3.0

    def can_run(self) -> bool:
        delta = time() - self.last_run
        if not self.is_running:
            if delta > self.cooldown:
                return True
            else:
                print(f"{self.keys} is on cooldown")
        else:
            print(f"{self.keys} is already running")
        return False

    def run(self) -> bool:
        if self.can_run():
            self.last_run = time()

            def fn() -> None:
                self.is_running = True
                self.fn(*self.args) # TODO kwargs?
                self.is_running = False

            Thread(target=fn).start()
            return True

        return False

def my_fn() -> None:
    sleep(0.5)
    print("SUCCESS")

def press_key_for(key: str, duration: float = 0) -> None:
    print(f"Pressing \"{key}\"")
    if duration:
        sleep(duration)
        print(f"Releasing \"{key}\"")

def press_key(key: str) -> None:
    press_key_for(key)


keys_forwards = "forward, leeroy jenkins"
keys_backwards = "backward, stop hammertime"
keys_left = "left, strafe left, walk left"

def split_csv(keys: str, delimiter: str = ',') -> list[str]:
    return [s.strip() for s in keys.split(delimiter)]

KeyboardControl = [
    Command(keys_forwards,  press_key_for, ['w', 1]),
    Command(keys_backwards, press_key_for, ['s', 1]),
    Command(keys_left,      press_key_for, ['a', 1])
]

chat_commands = [
    "forward",
    "stop hammertime",
    "walk left"
]

if __name__ == '__main__':
    flipflop = True

    for _ in range(10):
        if flipflop:
            sleep(1.1)
            flipflop = False
        else:
            sleep(0.1)
            flipflop = True

        chat_message = random.choice(chat_commands)

        found = False
        for command in KeyboardControl:
            keys = keys_to_list(command.keys)
            for key in keys:
                if chat_message.lower().strip().startswith(key):
                    command.run()
                    found = True
                    break
        if not found:
            print(f"Command not found: {chat_message}")