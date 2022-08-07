import logging

class KeyboardOutputs:
    @staticmethod
    def press_key_for(key: str, seconds: float = None):
        if seconds:
            logging.info("Press keyboard %s for %0.2fs", key, seconds)
        else:
            logging.info("Press keyboard %s", key)
    
    @staticmethod
    def press_key(key: str):
        return __class__.press_key_for(key)
        
class MouseOutputs:
    @staticmethod
    def press_button_for(button: str, seconds: float = None):
        if seconds:
            logging.info("Press mouse %s for %0.2fs", button, seconds)
        else:
            logging.info("Press mouse %s", button)
        
    @staticmethod
    def press_button(button: str):
        return __class__.press_button_for(button)
    
class LogOutputs:
    @staticmethod
    def log(logstr: str, level: int = logging.INFO):
        logging.log(level, logstr)
        
class PrintOutputs:
    @staticmethod
    def printer(*args: str):
        print(*args)