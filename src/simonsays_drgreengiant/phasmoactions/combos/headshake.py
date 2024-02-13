#!./.venv/bin/python3
import dataclasses
import random

from .... import actions, errorcodes, hidactions
from .. import defaults


@dataclasses.dataclass(slots=True)
class Headshake(defaults.GenericActionBase):
    """Look left and right repeatedly"""

    name: str = "headshake"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: HeadshakeConfig = self.config
        repeats = actionconfig.repeats
        pause = actionconfig.pause

        distance = actionconfig.distance or defaults.DEFAULTS.PEEK_DISTANCE

        lookleft = hidactions.MoveMouseRelativeDirectionSmooth(hidactions.MouseMoveDirectionSmoothActionConfig(distance, hidactions.MouseMoveDirection.LEFT))
        lookright = hidactions.MoveMouseRelativeDirectionSmooth(hidactions.MouseMoveDirectionSmoothActionConfig(distance, hidactions.MouseMoveDirection.RIGHT))

        once = actions.ActionSequence([lookleft, actions.Wait(pause), lookright])
        return actions.ActionRepeatWithWait(once, repeats, actions.Wait(pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class HeadshakeConfig:
    """Look left and right repeatedly config"""

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
