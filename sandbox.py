from time import sleep
from typing import Any, Optional, Callable
import multiprocessing as mp
import concurrent.futures
from threading import Thread

def mouse_click(button: str):
    print(f"Mouse click {button}")

def key_press(key: str):
    print(f"Key press {key}")

def key_press_hold(key: str, duration: str):
    t = float(duration)
    print(f"Key hold {key} for {t}")

KEYS = [
    ["a", 1, 0.1],
    ["b", 1, 0.1],
    ["c", 1, 0.1],
    ["d", 1, 0.1],
    ["e", 1, 0.1],
    ["f", 1, 0.1],
    ["g", 1, 0.1],
    ["h", 1, 0.1],
    ["i", 1, 0.1],
]

def press_release_routine(key: str, n_cycles: int, seconds: float = None) -> None:
    for _ in range(n_cycles):
        print(f"Press keyboard {key} for {seconds:.2f}s")
        sleep(seconds)
        print(f"Release keyboard {key} for {seconds:.2f}s")
        sleep(seconds)

if __name__ == '__main__':
    #mp.freeze_support()
    #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #with mp.Pool(processes=4) as pool:
        for key in KEYS:
            #pool.apply_async(press_release_routine, key)
            #executor.submit(press_release_routine, key)
            Thread(target=press_release_routine, args=key).start()
        sleep(10)