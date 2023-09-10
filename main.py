#!./.venv/bin/python3
import multiprocessing as mp
import platform

from src.simonsays_drgreengiant import simonsays

if __name__ == "__main__":
    if platform.platform().startswith("Windows"):
        # NOTE required for multiprocessing on Windows else it will bootloop
        mp.freeze_support()

    simonsays.main()
