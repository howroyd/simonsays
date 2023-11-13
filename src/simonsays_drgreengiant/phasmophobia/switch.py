#!./.venv/bin/python3
import dataclasses

from .. import environment, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Switch(GenericAction):
    """Switch to next inventory item"""
    name: str = "switch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class SwitchConfig:
    """Switch to next inventory item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.SWITCH))


def fp() -> set[gameactions.ActionConfigPair]:
    return set([gameactions.ActionConfigPair(Switch, SwitchConfig)])
