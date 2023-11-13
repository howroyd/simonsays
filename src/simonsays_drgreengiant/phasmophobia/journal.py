#!./.venv/bin/python3
import dataclasses

from .. import environment, gameactions, hidactions
from .defaults import DEFAULTS

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class JournalToggle(GenericAction):
    """Toggle the journal"""
    name: str = "journal"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class JournalToggleConfig:
    """Toggle the journal config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.JOURNAL))


def fp() -> set[gameactions.ActionConfigPair]:
    return set([gameactions.ActionConfigPair(JournalToggle, JournalToggleConfig)])
