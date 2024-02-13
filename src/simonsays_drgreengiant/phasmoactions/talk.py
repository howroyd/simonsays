#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Talk(defaults.GenericAction):
    """Toggle push to talk for a period of time"""

    name: str = "talk"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TalkConfig:
    """Toggle push to talk for a period of time config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.TALK))
    _duration: float = defaults.DEFAULTS.TALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration
