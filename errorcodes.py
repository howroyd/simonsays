#!./.venv/bin/python3
import enum
from collections.abc import Iterable


@enum.unique
class ErrorCode(enum.IntEnum):
    OK = 0
    UNKNOWN = enum.auto()
    NOT_IMPLEMENTED = enum.auto()
    DISABLED = enum.auto()
    ON_COOLDOWN = enum.auto()
    RANDOM_CHANCE = enum.auto()


ErrorSet = frozenset[ErrorCode]


def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def errorset(iter):
    return set(flatten(iter))
