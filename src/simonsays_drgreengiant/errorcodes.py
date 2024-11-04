#!./.venv/bin/python3
import enum
from collections.abc import Iterable
from typing import Any, TypeAlias


@enum.unique
class ErrorCode(enum.IntEnum):
    """Error codes"""

    OK = 0
    UNKNOWN = 1
    NOT_IMPLEMENTED = 2
    LOOKUP_FAILURE = 3
    DISABLED = 4
    ON_COOLDOWN = 5
    RANDOM_CHANCE = 6
    BLOCKED_USER = 7
    BLOCKED_CHANNEL = 8


ErrorSet: TypeAlias = set[ErrorCode]


def flatten(iter: Iterable[Any]) -> Any:
    """Flatten an iterable which may contain nested iterables"""
    for x in iter:
        if isinstance(x, Iterable) and not isinstance(x, str | bytes):
            yield from flatten(x)
        else:
            yield x


def errorset(errors: Iterable[ErrorCode] | ErrorCode) -> ErrorSet:
    """Make an error set"""
    if isinstance(errors, Iterable):
        return set(flatten(errors))
    elif isinstance(errors, ErrorCode):
        return set([errors])
    else:
        raise TypeError(f"Expected Iterable[ErrorCode] | ErrorCode, got {type(errors)}")


def success(errors: ErrorSet) -> bool:
    """Whether the error set is a success"""
    return ErrorCode.OK in errors and len(errors) == 1
