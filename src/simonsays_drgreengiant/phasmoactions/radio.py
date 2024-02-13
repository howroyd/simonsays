#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Radio(defaults.GenericAction):
    """Toggle global push to talk radio for a period of time"""

    name: str = "radio"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class RadioConfig:
    """Toggle global push to talk radio for a period of time config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.RADIO))
    _duration: float = defaults.DEFAULTS.TALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration
