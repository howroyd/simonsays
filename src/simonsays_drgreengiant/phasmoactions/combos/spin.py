#!./.venv/bin/python3
import dataclasses
import random

from ... import actions, errorcodes, hidactions
from .. import defaults, look


@dataclasses.dataclass(slots=True)
class Spin(defaults.GenericActionBase):
    """Spin on the spot"""

    name: str = "spin"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: SpinConfig = self.config

        direction = actionconfig.mousemovedirection or hidactions.MouseMoveDirection.RIGHT
        distance = actionconfig.distance or (look.LookRight().config.hidconfig.distance // 5)

        look_action = hidactions.MoveMouseRelativeDirection(hidactions.MouseMoveDirectionActionConfig(distance, direction))
        return actions.ActionRepeatWithWait(look_action, actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class SpinConfig:
    """Spin on the spot config"""

    hidconfig: hidactions.Config = None
    _pause: float = 0.015
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (25, 50))
    _mousemovedirection: hidactions.MouseMoveDirection = None
    _distance: int = defaults.DEFAULTS.LOOK_DISTANCE // 5

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
    def mousemovedirection(self) -> hidactions.MouseMoveDirection:
        """Get the mouse move direction"""
        return self._mousemovedirection or random.choice(list([hidactions.MouseMoveDirection.RIGHT, hidactions.MouseMoveDirection.LEFT]))

    @property
    def distance(self) -> int:
        """Get the distance"""
        return self._distance
