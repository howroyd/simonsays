import logging

import keyboard
from time import sleep
#import pyautogui
import pydirectinput


class KeyboardOutputs:
    @staticmethod
    def press_key_for(key: str, seconds: float = None) -> None:
        if seconds:
            logging.info("Press keyboard {key} for {seconds:.2f}s")
            keyboard.press(key)
            keyboard.call_later(__class__._release, (key,), seconds)
        else:
            logging.info("Press keyboard {key}")
            keyboard.press_and_release(key)

    @staticmethod
    def press_key(key: str) -> None:
        __class__.press_key_for(key)

    @staticmethod
    def _release(key: str) -> None:
        logging.info(f"Releasing {key}")
        keyboard.release(key)
class MouseOutputs:
    @staticmethod
    def press_button_for(button: str, seconds: float = 0.01) -> None:
        logging.info("Press mouse {button} for {seconds:.2f}s")
        pydirectinput.mouseDown(button=button)
        sleep(0.01) # Keep this short, else we need threads really
        pydirectinput.mouseUp(button=button)

    @staticmethod
    def press_button(button: str) -> None:
        __class__.press_button_for(button)

    @staticmethod
    def move(x: int, y: int) -> None:
        logging.info(f"Move mouse by x={x}, y={y}")
        pydirectinput.moveRel(x, y, 0.5, relative=True)

class LogOutputs:
    @staticmethod
    def log(logstr: str, level: int = logging.INFO) -> None:
        logging.log(level, logstr)

class PrintOutputs:
    @staticmethod
    def printer(*args: str) -> None:
        print(*args)