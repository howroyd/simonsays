#!./.venv/bin/python3
import dataclasses
import random

from .. import actions, environment, errorcodes, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class TorchToggle(GenericAction):
    """Toggle the torch"""
    name: str = "torch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TorchToggleConfig:
    """Toggle the torch config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.TORCH))


@dataclasses.dataclass(slots=True)
class Disco(GenericActionBase):
    """Turn the torch on and off repeatedly"""
    name: str = "disco"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: DiscoConfig = self.config
        return actions.ActionRepeatWithWait(TorchToggle(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class DiscoConfig:
    """Turn the torch on and off repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.33
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


def fp() -> set[gameactions.ActionConfigPair]:
    return set([
        gameactions.ActionConfigPair(TorchToggle, TorchToggleConfig),
        gameactions.ActionConfigPair(Disco, DiscoConfig),
    ])
