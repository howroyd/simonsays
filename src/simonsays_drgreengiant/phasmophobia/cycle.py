#!./.venv/bin/python3
import dataclasses
import random

from .. import actions, environment, errorcodes, gameactions, hidactions
from . import switch, use

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class CycleItems(GenericActionBase):
    """Cycle through the inventory repeatedly"""
    name: str = "cycle"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: CycleItemsConfig = self.config
        return actions.ActionRepeatWithWait(switch.Switch(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class CycleItemsConfig:
    """Cycle through the inventory repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.25
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))

    def __post_init__(self) -> None:
        if not isinstance(self._repeats, tuple):
            self._repeats = tuple(self._repeats)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return random.randint(*self._repeats)


@dataclasses.dataclass(slots=True)
class CycleItemsAndUse(GenericActionBase):
    """Cycle through the inventory and use the item, repeatedly"""
    name: str = "rekt"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: CycleItemsAndUseConfig = self.config
        sequence = actions.ActionSequence([switch.Switch(self.config_fn), actions.Wait(actionconfig.pause), use.Use(self.config_fn)])
        return actions.ActionRepeatWithWait(sequence, actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class CycleItemsAndUseConfig:
    """Cycle through the inventory and use the item, repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.25
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
        gameactions.ActionConfigPair(CycleItems, CycleItemsConfig),
        gameactions.ActionConfigPair(CycleItemsAndUse, CycleItemsAndUseConfig),
    ])
