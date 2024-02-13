#!./.venv/bin/python3
import dataclasses
import random

from ... import actions, errorcodes, hidactions
from .. import crouch, defaults


@dataclasses.dataclass(slots=True)
class Teabag(defaults.GenericActionBase):
    """Crouch repeatedly"""

    name: str = "teabag"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: TeabagConfig = self.config
        return actions.ActionRepeatWithWait(crouch.CrouchToggle(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class TeabagConfig:
    """Crouch repeatedly config"""

    hidconfig: hidactions.Config = None
    _pause: float = 0.5
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
