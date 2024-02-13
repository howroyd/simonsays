#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Drop(defaults.GenericAction):
    """Drop an item"""

    name: str = "drop"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class DropConfig:
    """Drop an item config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.DROP))
