#!./.venv/bin/python3
import dataclasses

from .. import environment, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Pickup(GenericAction):
    """Pickup an item"""
    name: str = "pickup"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PickupConfig:
    """Pickup an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.PICKUP))


def fp() -> set[gameactions.ActionConfigPair]:
    return set([gameactions.ActionConfigPair(Pickup, PickupConfig)])
