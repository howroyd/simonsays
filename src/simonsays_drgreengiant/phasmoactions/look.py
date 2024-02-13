#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class LookConfig:
    hidconfig: hidactions.Config


@dataclasses.dataclass(slots=True)
class LookUp(defaults.GenericAction):
    """Look up"""

    name: str = "look_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookUpConfig(LookConfig):
    """Look up config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.UP)
    )


@dataclasses.dataclass(slots=True)
class LookDown(defaults.GenericAction):
    """Look down"""

    name: str = "look_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookDownConfig(LookConfig):
    """Look down config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.DOWN)
    )


@dataclasses.dataclass(slots=True)
class LookLeft(defaults.GenericAction):
    """Look left"""

    name: str = "look_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookLeftConfig(LookConfig):
    """Look left config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.LEFT)
    )


@dataclasses.dataclass(slots=True)
class LookRight(defaults.GenericAction):
    """Look right"""

    name: str = "look_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookRightConfig(LookConfig):
    """Look right config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(defaults.DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.RIGHT)
    )
