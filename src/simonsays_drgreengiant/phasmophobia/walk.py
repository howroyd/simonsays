#!./.venv/bin/python3
import dataclasses
import enum
from typing import Any

from .. import actions, environment, errorcodes, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


class WalkDirectionUnknown(Exception):
    """Unknown walk direction"""
    pass


@enum.unique
class WalkDirection(enum.Enum):
    """Walk direction"""
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"

    def _missing_(self, value: Any) -> Any:
        """Handle missing values"""
        raise self.WalkDirectionUnknown(f"Unknown walk direction: {value}")

    def to_action(self) -> "Walk":
        """Convert a walk direction to an action"""
        match self:
            case self.FORWARD:
                return WalkForward
            case self.BACKWARD:
                return WalkBackward
            case self.LEFT:
                return WalkLeft
            case self.RIGHT:
                return WalkRight
            case _:
                raise WalkDirectionUnknown(f"Unknown walk direction: {self}")


@dataclasses.dataclass(slots=True)
class Walk(GenericAction):
    """Walk in a direction"""
    direction: WalkDirection
    name: str = dataclasses.field(init=False)
    chained: bool = False

    def __post_init__(self) -> None:
        self.name = self.direction.value

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: WalkConfig = self.config
        return hidactions.PressReleaseKeyOrButton(actionconfig.hidconfig, actionconfig.duration).run(force=force)


@dataclasses.dataclass(slots=True)
class WalkConfig:
    hidconfig: hidactions.Config
    _duration: float = DEFAULTS.WALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class WalkForward(Walk):
    """Walk forward"""
    direction: WalkDirection = WalkDirection.FORWARD


@dataclasses.dataclass(slots=True)
class WalkForwardConfig(WalkConfig):
    """Walk forward config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.FORWARD))


@dataclasses.dataclass(slots=True)
class WalkBackward(Walk):
    """Walk backward"""
    direction: WalkDirection = WalkDirection.BACKWARD


@dataclasses.dataclass(slots=True)
class WalkBackwardConfig(WalkConfig):
    """Walk backward config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.BACKWARD))


@dataclasses.dataclass(slots=True)
class WalkLeft(Walk):
    """Walk left"""
    direction: WalkDirection = WalkDirection.LEFT


@dataclasses.dataclass(slots=True)
class WalkLeftConfig(WalkConfig):
    """Walk left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.LEFT))


@dataclasses.dataclass(slots=True)
class WalkRight(Walk):
    """Walk right"""
    direction: WalkDirection = WalkDirection.RIGHT


@dataclasses.dataclass(slots=True)
class WalkRightConfig(WalkConfig):
    """Walk right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.RIGHT))


@dataclasses.dataclass(slots=True)
class Sprint(Walk):
    """Sprint in a direction"""

    def __post_init__(self) -> None:
        self.name = "sprint_" + self.direction.value

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: SprintConfig = self.config

        return actions.ActionSequence([
            hidactions.PressKeyOrButton(actionconfig.hidconfig),
            self.direction.to_action()(self.config_fn),
            hidactions.ReleaseKeyOrButton(actionconfig.hidconfig),
        ]).run(force=force)


@dataclasses.dataclass(slots=True)
class SprintConfig:
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.SPRINT))
    _duration: float = DEFAULTS.SPRINT_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class SprintForward(Sprint):
    """Sprint forward"""
    direction: WalkDirection = WalkDirection.FORWARD


@dataclasses.dataclass(slots=True)
class SprintBackward(Sprint):
    """Sprint backward"""
    direction: WalkDirection = WalkDirection.BACKWARD


@dataclasses.dataclass(slots=True)
class SprintLeft(Sprint):
    """Sprint left"""
    direction: WalkDirection = WalkDirection.LEFT


@dataclasses.dataclass(slots=True)
class SprintRight(Sprint):
    """Sprint right"""
    direction: WalkDirection = WalkDirection.RIGHT


def fp() -> set[gameactions.ActionConfigPair]:
    return set([
        gameactions.ActionConfigPair(WalkForward, WalkForwardConfig),
        gameactions.ActionConfigPair(WalkBackward, WalkBackwardConfig),
        gameactions.ActionConfigPair(WalkLeft, WalkLeftConfig),
        gameactions.ActionConfigPair(WalkRight, WalkRightConfig),
        gameactions.ActionConfigPair(SprintForward, SprintConfig),
        gameactions.ActionConfigPair(SprintBackward, SprintConfig),
        gameactions.ActionConfigPair(SprintLeft, SprintConfig),
        gameactions.ActionConfigPair(SprintRight, SprintConfig)
    ])
