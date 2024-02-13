#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Pickup(defaults.GenericAction):
    """Pickup an item"""

    name: str = "pickup"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PickupConfig:
    """Pickup an item config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.PICKUP))
