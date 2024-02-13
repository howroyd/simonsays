#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults, look

PeekConfig = look.LookConfig


@dataclasses.dataclass(slots=True)
class PeekUp(defaults.GenericAction):
    """Peek up"""

    name: str = "peek_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekUpConfig(PeekConfig):
    """Peek up config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.UP)
    )


@dataclasses.dataclass(slots=True)
class PeekDown(defaults.GenericAction):
    """Peek down"""

    name: str = "peek_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekDownConfig(PeekConfig):
    """Peek down config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.DOWN)
    )


@dataclasses.dataclass(slots=True)
class PeekLeft(defaults.GenericAction):
    """Peek left"""

    name: str = "peek_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekLeftConfig(PeekConfig):
    """Peek left config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.LEFT)
    )


@dataclasses.dataclass(slots=True)
class PeekRight(defaults.GenericAction):
    """Peek right"""

    name: str = "peek_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekRightConfig(PeekConfig):
    """Peek right config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.RIGHT)
    )
