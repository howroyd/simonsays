import logging

import keyboard, mouse
from time import sleep

def release(key: str):
    logging.info(f"Releasing {key}")
    keyboard.release(key)

class KeyboardOutputs:
    @staticmethod
    def press_key_for(key: str, seconds: float = None):
        if seconds:
            logging.info("Press keyboard %s for %0.2fs", key, seconds)
            keyboard.press(key)
            keyboard.call_later(release, (key,), seconds)
            #sleep(seconds)
            #keyboard.release(key)
        else:
            logging.info("Press keyboard %s", key)
            keyboard.press_and_release(key)

    @staticmethod
    def press_key(key: str):
        return __class__.press_key_for(key)

class MouseOutputs:
    @staticmethod
    def press_button_for(button: str, seconds: float = None):
        if seconds:
            logging.error("NOT IMPLEMENTED Press mouse %s for %0.2fs", button, seconds)
        else:
            logging.info("Press mouse %s", button)
            mouse.click(button)

    @staticmethod
    def press_button(button: str):
        return __class__.press_button_for(button)

    @staticmethod
    def move(x: int, y: int):
        logging.info(f"Move mouse by x={x}, y={y}")
        mouse.move(x, y, absolute=False, duration=0.5)

class LogOutputs:
    @staticmethod
    def log(logstr: str, level: int = logging.INFO):
        logging.log(level, logstr)

class PrintOutputs:
    @staticmethod
    def printer(*args: str):
        print(*args)