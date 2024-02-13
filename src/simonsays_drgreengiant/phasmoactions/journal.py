#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class JournalToggle(defaults.GenericAction):
    """Toggle the journal"""

    name: str = "journal"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class JournalToggleConfig:
    """Toggle the journal config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.JOURNAL))
