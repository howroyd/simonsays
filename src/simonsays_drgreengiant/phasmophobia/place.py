#!./.venv/bin/python3
import dataclasses

from .. import environment, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Place(GenericAction):
    """Place an item"""
    name: str = "place"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PlaceConfig:
    """Place an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.PLACE))


def fp() -> set[gameactions.ActionConfigPair]:
    return set([gameactions.ActionConfigPair(Place, PlaceConfig)])
