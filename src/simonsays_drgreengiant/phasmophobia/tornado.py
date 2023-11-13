#!./.venv/bin/python3
import dataclasses
import random

from .. import actions, environment, errorcodes, gameactions, hidactions
from . import defaults, drop, switch, use

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Tornado(GenericActionBase):
    """Spin on the spot whilst yeeting"""
    name: str = "tornado"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: TornadoConfig = self.config

        cfg = hidactions.MouseMoveDirectionSmoothActionConfig(actionconfig.distance,
                                                              actionconfig.mousemovedirection,
                                                              pause=actionconfig.pause)

        look = hidactions.MoveMouseRelativeDirectionSmooth(cfg)
        lookfar = actions.ActionRepeat(look, actionconfig.repeats)
        dropconfig = drop.Drop(self.config_fn).config.hidconfig
        dropaction = hidactions.PressReleaseKeyOrButton(dropconfig, delay=0.01)
        switchaction = switch.Switch(self.config_fn)

        lookanddrop = actions.ActionSequence([lookfar, dropaction, switchaction])

        return actions.ActionRepeat(lookanddrop, 4).run(force=force)


@dataclasses.dataclass(slots=True)
class TornadoConfig:
    """Spin on the spot whilst yeeting config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.005
    _repeats: int = 4
    _mousemovedirection: hidactions.MouseMoveDirection = None
    _distance: int = defaults.DEFAULTS.LOOK_DISTANCE

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return self._repeats

    @property
    def mousemovedirection(self) -> hidactions.MouseMoveDirection:
        """Get the mouse move direction"""
        return self._mousemovedirection or random.choice(list([hidactions.MouseMoveDirection.RIGHT, hidactions.MouseMoveDirection.LEFT]))

    @property
    def distance(self) -> int:
        """Get the distance"""
        return self._distance


@dataclasses.dataclass(slots=True)
class Hurricane(GenericActionBase):
    """Spin on the spot whilst using items"""
    name: str = "hurricane"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: TornadoConfig = self.config

        cfg = hidactions.MouseMoveDirectionSmoothActionConfig(actionconfig.distance,
                                                              actionconfig.mousemovedirection,
                                                              pause=actionconfig.pause)

        look = hidactions.MoveMouseRelativeDirectionSmooth(cfg)
        lookfar = actions.ActionRepeat(look, actionconfig.repeats)
        useconfig = use.Use(self.config_fn).config.hidconfig
        useaction = hidactions.PressReleaseKeyOrButton(useconfig, delay=0.01)
        dropconfig = drop.Drop(self.config_fn).config.hidconfig
        dropaction = hidactions.PressReleaseKeyOrButton(dropconfig, delay=0.01)
        switchaction = switch.Switch(self.config_fn)

        lookanduse = actions.ActionSequence([lookfar, useaction, dropaction, switchaction])

        return actions.ActionRepeat(lookanduse, 4).run(force=force)


@dataclasses.dataclass(slots=True)
class HurricaneConfig:
    """Spin on the spot whilst using items config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.005
    _repeats: int = 4
    _mousemovedirection: hidactions.MouseMoveDirection = None
    _distance: int = defaults.DEFAULTS.LOOK_DISTANCE

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return self._repeats

    @property
    def mousemovedirection(self) -> hidactions.MouseMoveDirection:
        """Get the mouse move direction"""
        return self._mousemovedirection or random.choice(list([hidactions.MouseMoveDirection.RIGHT, hidactions.MouseMoveDirection.LEFT]))

    @property
    def distance(self) -> int:
        """Get the distance"""
        return self._distance


def fp() -> set[gameactions.ActionConfigPair]:
    return set([
        gameactions.ActionConfigPair(Tornado, TornadoConfig),
        gameactions.ActionConfigPair(Hurricane, HurricaneConfig),
    ])
