#!./.venv/bin/python3
import dataclasses

from ... import hidactions
from .. import defaults, look


@dataclasses.dataclass(slots=True)
class Yoga(defaults.GenericAction):
    """Look up to the sky"""

    name: str = "yoga"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class YogaConfig(look.LookConfig):
    """Look up to the sky config"""

    hidconfig: hidactions.Config = dataclasses.field(
        default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(4096, hidactions.MouseMoveDirection.UP, pause=0.0025, repeats=100)
    )
