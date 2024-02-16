#!./.venv/bin/python3
import dataclasses
import random
from collections.abc import Callable

from .. import errorcodes, gameactions, hidactions
from . import crouch, defaults, drop, journal, look, peek, pickup, place, radio, sprint, switch, talk, torch, use, walk
from .combos import box, cycle, cycleuse, disco, dropall, feet, freeze, headbang, headshake, hurricane, spin, teabag, tornado, yoga


@dataclasses.dataclass(slots=True)
class RandomAction(defaults.GenericActionBase):
    """Pick a random action and run it"""

    # TODO can this be generalised into actions.RandomAction?
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


def _get_all() -> gameactions.ActionAndConfigDict:
    return {
        crouch.CrouchToggle(None).name: gameactions.ActionAndConfig(crouch.CrouchToggle, crouch.CrouchToggleConfig()),
        drop.Drop(None).name: gameactions.ActionAndConfig(drop.Drop, drop.DropConfig()),
        journal.JournalToggle(None).name: gameactions.ActionAndConfig(journal.JournalToggle, journal.JournalToggleConfig()),
        look.LookUp(None).name: gameactions.ActionAndConfig(look.LookUp, look.LookUpConfig()),
        look.LookDown(None).name: gameactions.ActionAndConfig(look.LookDown, look.LookDownConfig()),
        look.LookLeft(None).name: gameactions.ActionAndConfig(look.LookLeft, look.LookLeftConfig()),
        look.LookRight(None).name: gameactions.ActionAndConfig(look.LookRight, look.LookRightConfig()),
        peek.PeekUp(None).name: gameactions.ActionAndConfig(peek.PeekUp, peek.PeekUpConfig()),
        peek.PeekDown(None).name: gameactions.ActionAndConfig(peek.PeekDown, peek.PeekDownConfig()),
        peek.PeekLeft(None).name: gameactions.ActionAndConfig(peek.PeekLeft, peek.PeekLeftConfig()),
        peek.PeekRight(None).name: gameactions.ActionAndConfig(peek.PeekRight, peek.PeekRightConfig()),
        pickup.Pickup(None).name: gameactions.ActionAndConfig(pickup.Pickup, pickup.PickupConfig()),
        place.Place(None).name: gameactions.ActionAndConfig(place.Place, place.PlaceConfig()),
        radio.Radio(None).name: gameactions.ActionAndConfig(radio.Radio, radio.RadioConfig()),
        sprint.SprintForward(None).name: gameactions.ActionAndConfig(sprint.SprintForward, sprint.SprintConfig()),
        sprint.SprintBackward(None).name: gameactions.ActionAndConfig(sprint.SprintBackward, sprint.SprintConfig()),
        sprint.SprintLeft(None).name: gameactions.ActionAndConfig(sprint.SprintLeft, sprint.SprintConfig()),
        sprint.SprintRight(None).name: gameactions.ActionAndConfig(sprint.SprintRight, sprint.SprintConfig()),
        switch.Switch(None).name: gameactions.ActionAndConfig(switch.Switch, switch.SwitchConfig()),
        talk.Talk(None).name: gameactions.ActionAndConfig(talk.Talk, talk.TalkConfig()),
        torch.TorchToggle(None).name: gameactions.ActionAndConfig(torch.TorchToggle, torch.TorchToggleConfig()),
        use.Use(None).name: gameactions.ActionAndConfig(use.Use, use.UseConfig()),
        walk.WalkForward(None).name: gameactions.ActionAndConfig(walk.WalkForward, walk.WalkForwardConfig()),
        walk.WalkBackward(None).name: gameactions.ActionAndConfig(walk.WalkBackward, walk.WalkBackwardConfig()),
        walk.WalkLeft(None).name: gameactions.ActionAndConfig(walk.WalkLeft, walk.WalkLeftConfig()),
        walk.WalkRight(None).name: gameactions.ActionAndConfig(walk.WalkRight, walk.WalkRightConfig()),
        box.Box(None).name: gameactions.ActionAndConfig(box.Box, box.BoxConfig()),
        cycle.CycleItems(None).name: gameactions.ActionAndConfig(cycle.CycleItems, cycle.CycleItemsConfig()),
        cycleuse.CycleItemsAndUse(None).name: gameactions.ActionAndConfig(cycleuse.CycleItemsAndUse, cycleuse.CycleItemsAndUseConfig()),
        disco.Disco(None).name: gameactions.ActionAndConfig(disco.Disco, disco.DiscoConfig()),
        dropall.DropAllItems(None).name: gameactions.ActionAndConfig(dropall.DropAllItems, dropall.DropAllItemsConfig()),
        feet.Feet(None).name: gameactions.ActionAndConfig(feet.Feet, feet.FeetConfig()),
        freeze.Freeze(None).name: gameactions.ActionAndConfig(freeze.Freeze, freeze.FreezeConfig()),
        headbang.Headbang(None).name: gameactions.ActionAndConfig(headbang.Headbang, headbang.HeadbangConfig()),
        headshake.Headshake(None).name: gameactions.ActionAndConfig(headshake.Headshake, headshake.HeadshakeConfig()),
        hurricane.Hurricane(None).name: gameactions.ActionAndConfig(hurricane.Hurricane, hurricane.HurricaneConfig()),
        spin.Spin(None).name: gameactions.ActionAndConfig(spin.Spin, spin.SpinConfig()),
        teabag.Teabag(None).name: gameactions.ActionAndConfig(teabag.Teabag, teabag.TeabagConfig()),
        tornado.Tornado(None).name: gameactions.ActionAndConfig(tornado.Tornado, tornado.TornadoConfig()),
        yoga.Yoga(None).name: gameactions.ActionAndConfig(yoga.Yoga, yoga.YogaConfig()),
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
    return [T.actiontype(config_fn) for T in _get_all().values()]


def all_actions_dict(config_fn: gameactions.ConfigFn) -> gameactions.ActionDict:
    """Get all actions as a dict"""
    return {action.name: action for action in all_actions(config_fn)}


def default_config() -> gameactions.Config:
    """Get the default config"""
    return gameactions.Config({k: v.config for k, v in _get_all().items()})
