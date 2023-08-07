#!./.venv/bin/python3
import enum
from collections.abc import Iterable


@enum.unique
class ErrorCode(enum.IntEnum):
    """Error codes"""
    OK = 0
    UNKNOWN = enum.auto()
    NOT_IMPLEMENTED = enum.auto()
    LOOKUP_FAILURE = enum.auto()
    DISABLED = enum.auto()
    ON_COOLDOWN = enum.auto()
    RANDOM_CHANCE = enum.auto()


ErrorSet = set[ErrorCode]


def flatten(xs):
    """Flatten an iterable"""
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
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
