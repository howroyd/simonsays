#!./.venv/bin/python3
import dataclasses

from .. import environment, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Use(GenericAction):
    """Use item"""
    name: str = "use"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class UseConfig:
    """Use item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseButtonActionConfig(DEFAULTS.KEYBINDS.USE))


def fp() -> set[gameactions.ActionConfigPair]:
    return set([gameactions.ActionConfigPair(Use, UseConfig)])
