#!./.venv/bin/python3
import dataclasses

from .. import actions, errorcodes, hidactions
from . import defaults, walk


@dataclasses.dataclass(slots=True)
class Sprint(walk.Walk):
    """Sprint in a direction"""

    def __post_init__(self) -> None:
        self.name = "sprint_" + self.direction.value

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: SprintConfig = self.config

        return actions.ActionSequence(
            [
                hidactions.PressKeyOrButton(actionconfig.hidconfig),
                self.direction.to_action()(self.config_fn),
                hidactions.ReleaseKeyOrButton(actionconfig.hidconfig),
            ]
        ).run(force=force)


@dataclasses.dataclass(slots=True)
class SprintConfig:
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.SPRINT))
    _duration: float = defaults.DEFAULTS.SPRINT_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class SprintForward(Sprint):
    """Sprint forward"""

    direction: walk.WalkDirection = walk.WalkDirection.FORWARD


@dataclasses.dataclass(slots=True)
class SprintBackward(Sprint):
    """Sprint backward"""

    direction: walk.WalkDirection = walk.WalkDirection.BACKWARD


@dataclasses.dataclass(slots=True)
class SprintLeft(Sprint):
    """Sprint left"""

    direction: walk.WalkDirection = walk.WalkDirection.LEFT


@dataclasses.dataclass(slots=True)
class SprintRight(Sprint):
    """Sprint right"""

    direction: walk.WalkDirection = walk.WalkDirection.RIGHT
