#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Use(defaults.GenericAction):
    """Use item"""

    name: str = "use"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class UseConfig:
    """Use item config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseButtonActionConfig(defaults.DEFAULTS.KEYBINDS.USE))
