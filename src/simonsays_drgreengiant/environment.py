#!./.venv/bin/python3
import os

TRUTHYSTRINGS = frozenset(('true', '1', 'yes'))  # Add more entries if you want, like: `y`, `yes`, `on`, ...
FALSYSTRINGS = frozenset(('false', '0', 'no'))  # Add more entries if you want, like: `n`, `no`, `off`, ...


def getenvboolean(name: str, default_value: bool | None = None) -> bool:
    value: str | None = os.getenv(name, None)
    if not value:
        if default_value is None:
            raise ValueError(f'Variable `{name}` not set!')
        else:
            value = str(default_value)
    if value.lower() not in frozenset.union(*[TRUTHYSTRINGS, FALSYSTRINGS]):
        raise ValueError(f'Invalid value `{value}` for variable `{name}`')
    return value in TRUTHYSTRINGS
