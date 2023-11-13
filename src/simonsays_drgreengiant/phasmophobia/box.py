#!./.venv/bin/python3
import dataclasses

from .. import actions, environment, errorcodes, gameactions, hidactions
from . import drop, use

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class Box(GenericAction):
    """Music box grenade; use and drop"""
    name: str = "box"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: BoxConfig = self.config
        return actions.ActionSequence([use.Use(self.config_fn), actions.Wait(actionconfig.pause), drop.Drop(self.config_fn)]).run(force=force)


@dataclasses.dataclass(slots=True)
class BoxConfig:
    """Use item config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.5

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause


def fp() -> set[gameactions.ActionConfigPair]:
    return set([gameactions.ActionConfigPair(Box, BoxConfig)])
