#!./.venv/bin/python3
import dataclasses

from .. import actions, environment, errorcodes, gameactions, hidactions
from . import switch
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Drop(GenericAction):
    """Drop an item"""
    name: str = "drop"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class DropConfig:
    """Drop an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.DROP))


@dataclasses.dataclass(slots=True)
class DropAllItems(GenericActionBase):
    """Cycle through the inventory and drop each item"""
    name: str = "yeet"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: DropAllItemsConfig = self.config
        sequence = actions.ActionSequence([Drop(self.config_fn), actions.Wait(actionconfig.pause), switch.Switch(self.config_fn)])
        return actions.ActionRepeatWithWait(sequence, actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class DropAllItemsConfig:
    """Cycle through the inventory and drop each item config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.10
    _repeats: int = 3

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return self._repeats


def fp() -> set[gameactions.ActionConfigPair]:
    return set([
        gameactions.ActionConfigPair(Drop, DropConfig),
        gameactions.ActionConfigPair(DropAllItems, DropAllItemsConfig),
    ])
