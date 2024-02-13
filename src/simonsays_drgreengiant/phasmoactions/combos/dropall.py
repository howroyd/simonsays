#!./.venv/bin/python3
import dataclasses

from .... import actions, errorcodes, hidactions
from .. import defaults, drop, switch


@dataclasses.dataclass(slots=True)
class DropAllItems(defaults.GenericActionBase):
    """Cycle through the inventory and drop each item"""

    name: str = "yeet"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: DropAllItemsConfig = self.config
        sequence = actions.ActionSequence([drop.Drop(self.config_fn), actions.Wait(actionconfig.pause), switch.Switch(self.config_fn)])
        return actions.ActionRepeatWithWait(sequence, actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class DropAllItemsConfig:
    """Cycle through the inventory and drop each item config"""

    hidconfig: hidactions.Config = None
    _pause: float = 0.10
    _repeats: int = 3

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return self._repeats
