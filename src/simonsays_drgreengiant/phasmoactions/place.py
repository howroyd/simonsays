#!./.venv/bin/python3
import dataclasses

from .. import hidactions
from . import defaults


@dataclasses.dataclass(slots=True)
class Place(defaults.GenericAction):
    """Place an item"""

    name: str = "place"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PlaceConfig:
    """Place an item config"""

    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(defaults.DEFAULTS.KEYBINDS.PLACE))
