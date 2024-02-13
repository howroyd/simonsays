#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class TorchToggle(defaults.GenericAction):
    """Toggle the torch"""

    name: str = "torch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TorchToggleConfig:
    """Toggle the torch config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.TORCH))
