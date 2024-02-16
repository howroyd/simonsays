#!./.venv/bin/python3
import dataclasses

from ... import actions, errorcodes, hidactions
from .. import defaults, switch, use


@dataclasses.dataclass(slots=True)
class CycleItemsAndUse(defaults.GenericActionBase):
    """Cycle through the inventory and use the item, repeatedly"""

    name: str = "rekt"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: CycleItemsAndUseConfig = self.config
        sequence = actions.ActionSequence([switch.Switch(self.config_fn), actions.Wait(actionconfig.pause), use.Use(self.config_fn)])
        return actions.ActionRepeatWithWait(sequence, actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class CycleItemsAndUseConfig:
    """Cycle through the inventory and use the item, repeatedly config"""

    hidconfig: hidactions.Config = None
    _pause: float = 0.25
    _repeats: int = 3

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return self._repeats
