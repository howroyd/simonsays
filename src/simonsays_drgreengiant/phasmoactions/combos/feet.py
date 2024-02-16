#!./.venv/bin/python3
import dataclasses

from ... import hidactions
from .. import defaults, look


@dataclasses.dataclass(slots=True)
class Feet(defaults.GenericAction):
    """Look down to the floor"""

    name: str = "feet"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class FeetConfig(look.LookConfig):
    """Look down to the floor config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(4096, hidactions.MouseMoveDirection.DOWN, pause=0.0025, repeats=100)
    )
