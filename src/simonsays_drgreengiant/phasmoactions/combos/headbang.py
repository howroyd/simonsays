#!./.venv/bin/python3
import dataclasses
import random

from .... import actions, errorcodes, hidactions
from .. import defaults


@dataclasses.dataclass(slots=True)
class Headbang(defaults.GenericActionBase):
    """Look up and down repeatedly"""

    name: str = "headbang"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: HeadbangConfig = self.config
        repeats = actionconfig.repeats
        pause = actionconfig.pause

        distance = actionconfig.distance or defaults.DEFAULTS.PEEK_DISTANCE

        lookup = hidactions.MoveMouseRelativeDirectionSmooth(hidactions.MouseMoveDirectionSmoothActionConfig(distance, hidactions.MouseMoveDirection.UP))
        lookdown = hidactions.MoveMouseRelativeDirectionSmooth(hidactions.MouseMoveDirectionSmoothActionConfig(distance, hidactions.MouseMoveDirection.DOWN))

        once = actions.ActionSequence([lookup, actions.Wait(pause), lookdown])
        return actions.ActionRepeatWithWait(once, repeats, actions.Wait(pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class HeadbangConfig:
    """Look up and down repeatedly config"""

    hidconfig: hidactions.Config = None
    _pause: float = 0.33
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))
    _distance: int = defaults.DEFAULTS.PEEK_DISTANCE

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

    @property
    def distance(self) -> int:
        """Get the distance"""
        return self._distance
