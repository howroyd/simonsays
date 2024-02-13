#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Switch(defaults.GenericAction):
    """Switch to next inventory item"""

    name: str = "switch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class SwitchConfig:
    """Switch to next inventory item config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.SWITCH))
