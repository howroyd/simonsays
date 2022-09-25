import logging

from time import sleep
from threading import Thread

from pynput.keyboard import Key
from pynput.keyboard import Controller as Keyboard

from pynput.mouse._win32 import Button
from pynput.mouse._win32 import Controller as Mouse

keyboard = Keyboard()
mouse    = Mouse()

def str_to_button(button: str) -> Button:
    match button:
        case "left":
            return Button.left
        case "middle":
            return Button.middle
        case "right":
            return Button.right
        case _:
            raise KeyError

class KeyboardOutputs:
    @staticmethod
    def press_release_routine(key: str, n_cycles: int, seconds: float = None) -> None:
        for _ in range(n_cycles):
            logging.info(f"Press keyboard {key} then wait {seconds:.2f}s")
            keyboard.press(key)
            sleep(0.01)
            keyboard.release(key)
            sleep(seconds)

    @staticmethod
    def press_key_for(key: str, seconds: float = None) -> None:
        if seconds:
            logging.info(f"Press keyboard {key} for {seconds:.2f}s")
            keyboard.press(key)
            x = Thread(target=__class__._release_later, args=(key, seconds))
            x.start()
        else:
            logging.info(f"Press keyboard {key}")
            keyboard.press(key)
            keyboard.release(key)

    @staticmethod
    def press_key(key: str) -> None:
        __class__.press_key_for(key)

    @staticmethod
    def _release_later(key: str, seconds: float = None) -> None:
        sleep(seconds)
        logging.info(f"Releasing {key}")
        keyboard.release(key)

    @staticmethod
    def _release(key: str) -> None:
        __class__._release_later(key)

class MouseOutputs:
    @staticmethod
    def press_button_for(button: str, seconds: float = 0.01) -> None:
        logging.info(f"Press mouse {button} for {seconds:.2f}s")
        pybutton = str_to_button(button)

        if seconds < 0.05:
            mouse.press(pybutton)
            sleep(seconds)
            mouse.release(pybutton)
        else:
            mouse.press(button)
            x = Thread(target=__class__._release_later, args=(button, seconds))
            x.start()

    @staticmethod
    def press_button(button: str) -> None:
        __class__.press_button_for(button)

    @staticmethod
    def move_routine(x: int, y: int, seconds: float) -> None:
        steps = max(abs(x), abs(y))
        timestep = seconds / steps
        logging.info(f"Move mouse by x={x}, y={y} in {seconds}s ({steps} steps {timestep}s apart)")
        for _ in range(steps):
            mouse.move(x // steps, y // steps)
            sleep(timestep)

    @staticmethod
    def move(x: int, y: int) -> None:
        logging.info(f"Move mouse by x={x}, y={y}")
        mouse.move(x, y)

    @staticmethod
    def _release_later(button: str, seconds: float = None) -> None:
        pybutton = str_to_button(button)
        sleep(seconds)
        logging.info(f"Releasing {button}")
        mouse.release(pybutton)

    @staticmethod
    def _release(button: str) -> None:
        __class__._release_later(button)

class LogOutputs:
    @staticmethod
    def log(logstr: str, level: int = logging.INFO) -> None:
        logging.log(level, logstr)

class PrintOutputs:
    @staticmethod
    def printer(*args: str) -> None:
        print(*args)