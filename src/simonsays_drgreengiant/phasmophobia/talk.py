#!./.venv/bin/python3
import dataclasses

from .. import environment, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Talk(GenericAction):
    """Toggle push to talk for a period of time"""
    name: str = "talk"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TalkConfig:
    """Toggle push to talk for a period of time config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.TALK))
    _duration: float = DEFAULTS.TALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class Radio(GenericAction):
    """Toggle global push to talk radio for a period of time"""
    name: str = "radio"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class RadioConfig:
    """Toggle global push to talk radio for a period of time config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.RADIO))
    _duration: float = DEFAULTS.TALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


def fp() -> set[gameactions.ActionConfigPair]:
    return set([
        gameactions.ActionConfigPair(Talk, TalkConfig),
        gameactions.ActionConfigPair(Radio, RadioConfig),
    ])
