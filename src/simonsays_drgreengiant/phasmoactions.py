#!./.venv/bin/python3
import dataclasses
import random
from typing import Callable

from . import errorcodes, gameactions, hidactions
from .phasmophobia import (box, crouch, cycle, drop, freeze, journal, look,
                           pickup, place, spin, switch, talk, torch, tornado,
                           use, walk)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True)
class RandomAction(GenericActionBase):
    """Pich a random action and run it"""
    name: str = "random"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        tag, randomaction = random.choice([(k, v) for k, v in self.config.actiondict.items() if k != self.name])
        print(f"RandomAction: {tag}")
        return randomaction.run()


@dataclasses.dataclass(slots=True)
class RandomActionConfig:
    """Look up and down repeatedly config"""
    _actiondict: Callable[[], gameactions.ActionDict]
    hidconfig: hidactions.Config = None

    @property
    def actiondict(self) -> gameactions.ActionDict:
        """Get the action dictionary"""
        return self._actiondict()


#####################################################################

def _all_fp() -> set[gameactions.ActionConfigPair]:
    """Collating all the action function pointers"""
    return (
        crouch.fp() |  # noqa: W504
        drop.fp() |  # noqa: W504
        journal.fp() |  # noqa: W504
        look.fp() |  # noqa: W504
        pickup.fp() |  # noqa: W504
        place.fp() |  # noqa: W504
        switch.fp() |  # noqa: W504
        talk.fp() |  # noqa: W504
        torch.fp() |  # noqa: W504
        use.fp() |  # noqa: W504
        walk.fp() |  # noqa: W504
        box.fp() |  # noqa: W504
        cycle.fp() |  # noqa: W504
        spin.fp() |  # noqa: W504
        freeze.fp() |  # noqa: W504
        tornado.fp()  # noqa: W504
    )


def _get_all(config_fn: gameactions.ConfigFn) -> gameactions.ActionAndConfigDict:
    return {
        fp.action(None).name: gameactions.ActionAndConfig(fp.action, fp.config) for fp in _all_fp()
    }


@dataclasses.dataclass(slots=True)
class PhasmoActions:
    masterdict: gameactions.ActionAndConfigDict = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.masterdict = _get_all(lambda: self.config_fn)

    @property
    def tags(self) -> list[str]:
        """Get all tags"""
        return list(self.masterdict.keys())

    @property
    def actions(self) -> gameactions.ActionDict:
        """Get all actions"""
        return {tag: actionandconfig.action for tag, actionandconfig in self.masterdict.items()}

    @property
    def configs(self) -> gameactions.ConfigDict:
        """Get all configs"""
        return {tag: actionandconfig.config for tag, actionandconfig in self.masterdict.items()}

    def action_of(self, tag: str) -> gameactions.Action | None:
        """Get the action for the tag"""
        return self.masterdict[tag].action


def all_actions(config_fn: gameactions.ConfigFn) -> list[gameactions.Action]:
    """Get all actions"""
    return [
        fp.action(config_fn) for fp in _all_fp()
    ]


def all_actions_dict(config_fn: gameactions.ConfigFn) -> gameactions.ActionDict:
    """Get all actions as a dict"""
    return {action.name: action for action in all_actions(config_fn)}


def default_config() -> gameactions.Config:
    """Get the default config"""
    return gameactions.Config(
        {fp.action(None).name: fp.config() for fp in _all_fp()}
    )
