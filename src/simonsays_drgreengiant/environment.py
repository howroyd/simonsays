#!./.venv/bin/python3
import os
import sys
from typing import Any

TRUTHYSTRINGS = frozenset(("true", "1", "yes"))  # Add more entries if you want, like: `y`, `yes`, `on`, ...
FALSYSTRINGS = frozenset(("false", "0", "no"))  # Add more entries if you want, like: `n`, `no`, `off`, ...


def resource_path(*paths: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, *paths) if paths else base_path


def update_env() -> None:
    """Update the environment variables"""
    # DATAPATH = os.path.dirname(sys.modules["simonsays_drgreengiant"].__file__)
    DATAPATH = resource_path()

    newvars = {}

    try:
        with open(os.path.join(DATAPATH, ".env"), "r") as f:
            # with open(DATAPATH, "r") as f:
            for line in f.readlines():
                thisline = line.strip()
                if thisline.startswith("#") or "=" not in thisline:
                    continue
                key, value = thisline.split("=", 1)
                newvars[key] = value
        os.environ.update(newvars)
    except FileNotFoundError:
        pass


update_env()


def getenv(name: str, default_value: str | Any = None) -> str | Any:
    """Get an environment variable"""
    return os.getenv(name, default_value)


def getenvboolean(name: str, default_value: bool | None = None) -> bool:
    """Get an environment variable as a boolean"""
    value = getenv(name)
    if not value:
        if default_value is None:
            raise ValueError(f"Variable `{name}` not set!")
        else:
            value = str(default_value)
    if value.lower() not in frozenset.union(*[TRUTHYSTRINGS, FALSYSTRINGS]):
        raise ValueError(f"Invalid value `{value}` for variable `{name}`")
    return value in TRUTHYSTRINGS
