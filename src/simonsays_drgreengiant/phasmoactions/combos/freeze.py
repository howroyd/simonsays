#!./.venv/bin/python3
import dataclasses

from ... import actions, errorcodes, hidactions
from .. import defaults, walk


@dataclasses.dataclass(slots=True)
class Freeze(defaults.GenericActionBase):
    """Counterstrafe to freeze on the spot"""

    name: str = "freeze"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: FreezeConfig = self.config

        forwardPress = hidactions.PressKeyOrButton(walk.WalkForwardConfig().hidconfig)
        rightPress = hidactions.PressKeyOrButton(walk.WalkRightConfig().hidconfig)
        backwardPress = hidactions.PressKeyOrButton(walk.WalkBackwardConfig().hidconfig)
        leftPress = hidactions.PressKeyOrButton(walk.WalkLeftConfig().hidconfig)

        press = actions.ActionSequence([forwardPress, rightPress, backwardPress, leftPress])

        forwardRelease = hidactions.ReleaseKeyOrButton(walk.WalkForwardConfig().hidconfig)
        rightRelease = hidactions.ReleaseKeyOrButton(walk.WalkRightConfig().hidconfig)
        backwardRelease = hidactions.ReleaseKeyOrButton(walk.WalkBackwardConfig().hidconfig)
        leftRelease = hidactions.ReleaseKeyOrButton(walk.WalkLeftConfig().hidconfig)

        release = actions.ActionSequence([forwardRelease, rightRelease, backwardRelease, leftRelease])

        once = actions.ActionSequence([press, actions.Wait(actionconfig.pause), release, actions.Wait(actionconfig.pause)])

        return actions.ActionRepeat(once, actionconfig.repeats).run(force=force)


@dataclasses.dataclass(slots=True)
class FreezeConfig:
    """Counterstrafe to freeze on the spot config"""

    hidconfig: hidactions.Config = None
    _pause: float = 0.01
    _repeats: int = int(5 / 4 / 0.01)

    def __post_init__(self) -> None:
        self._repeats = int(5.0 / 4.0 / self._pause)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return self._repeats
