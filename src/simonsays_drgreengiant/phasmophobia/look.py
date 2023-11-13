#!./.venv/bin/python3
import dataclasses
import random

from .. import actions, environment, errorcodes, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class LookConfig:
    hidconfig: hidactions.Config


@dataclasses.dataclass(slots=True)
class LookUp(GenericAction):
    """Look up"""
    name: str = "look_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookUpConfig(LookConfig):
    """Look up config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class LookDown(GenericAction):
    """Look down"""
    name: str = "look_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookDownConfig(LookConfig):
    """Look down config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.DOWN))


@dataclasses.dataclass(slots=True)
class LookLeft(GenericAction):
    """Look left"""
    name: str = "look_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookLeftConfig(LookConfig):
    """Look left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.LEFT))


@dataclasses.dataclass(slots=True)
class LookRight(GenericAction):
    """Look right"""
    name: str = "look_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookRightConfig(LookConfig):
    """Look right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.RIGHT))


@dataclasses.dataclass(slots=True)
class Yoga(GenericAction):
    """Look up to the sky"""
    name: str = "yoga"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class YogaConfig(LookConfig):
    """Look up to the sky config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(4096, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class Feet(GenericAction):
    """Look down to the floor"""
    name: str = "feet"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class FeetConfig(LookConfig):
    """Look down to the floor config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(4096, hidactions.MouseMoveDirection.DOWN))


PeekConfig = LookConfig


@dataclasses.dataclass(slots=True)
class PeekUp(GenericAction):
    """Peek up"""
    name: str = "peek_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekUpConfig(PeekConfig):
    """Peek up config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class PeekDown(GenericAction):
    """Peek down"""
    name: str = "peek_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekDownConfig(PeekConfig):
    """Peek down config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.DOWN))


@dataclasses.dataclass(slots=True)
class PeekLeft(GenericAction):
    """Peek left"""
    name: str = "peek_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekLeftConfig(PeekConfig):
    """Peek left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.LEFT))


@dataclasses.dataclass(slots=True)
class PeekRight(GenericAction):
    """Peek right"""
    name: str = "peek_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekRightConfig(PeekConfig):
    """Peek right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.RIGHT))


@dataclasses.dataclass(slots=True)
class Headbang(GenericActionBase):
    """Look up and down repeatedly"""
    name: str = "headbang"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: HeadbangConfig = self.config
        repeats = actionconfig.repeats
        pause = actionconfig.pause

        if DEBUG:
            print(f"Headbang: repeats={repeats}, pause={pause}")

        distance = actionconfig.distance or DEFAULTS.PEEK_DISTANCE

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
    _distance: int = DEFAULTS.PEEK_DISTANCE

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

#####################################################################


@dataclasses.dataclass(slots=True)
class Headshake(GenericActionBase):
    """Look left and right repeatedly"""
    name: str = "headshake"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: HeadshakeConfig = self.config
        repeats = actionconfig.repeats
        pause = actionconfig.pause

        if DEBUG:
            print(f"Headshake: repeats={repeats}, pause={pause}")

        distance = actionconfig.distance or DEFAULTS.PEEK_DISTANCE

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
    _distance: int = DEFAULTS.PEEK_DISTANCE

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


def fp() -> set[gameactions.ActionConfigPair]:
    return set([
        gameactions.ActionConfigPair(LookUp, LookUpConfig),
        gameactions.ActionConfigPair(LookDown, LookDownConfig),
        gameactions.ActionConfigPair(LookLeft, LookLeftConfig),
        gameactions.ActionConfigPair(LookRight, LookRightConfig),
        gameactions.ActionConfigPair(Yoga, YogaConfig),
        gameactions.ActionConfigPair(Feet, FeetConfig),
        gameactions.ActionConfigPair(PeekUp, PeekUpConfig),
        gameactions.ActionConfigPair(PeekDown, PeekDownConfig),
        gameactions.ActionConfigPair(PeekLeft, PeekLeftConfig),
        gameactions.ActionConfigPair(PeekRight, PeekRightConfig),
        gameactions.ActionConfigPair(Headbang, HeadbangConfig),
        gameactions.ActionConfigPair(Headshake, HeadshakeConfig),
    ])
