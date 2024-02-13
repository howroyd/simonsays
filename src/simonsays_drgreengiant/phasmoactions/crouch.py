#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class CrouchToggle(defaults.GenericAction):
    """Toggle crouch"""

    name: str = "crouch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class CrouchToggleConfig:
    """Toggle crouch config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.CROUCH))
