#!./.venv/bin/python3
import dataclasses
import random
from collections.abc import Callable

from .. import phasmoactions as pa
from . import errorcodes, gameactions, hidactions


@dataclasses.dataclass(slots=True)
class RandomAction(pa.defaults.GenericActionBase):
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


def _get_all(config_fn: gameactions.ConfigFn) -> gameactions.ActionAndConfigDict:
    return {
        pa.WalkForward(None).name: gameactions.ActionAndConfig(pa.WalkForward, pa.WalkForwardConfig()),
        pa.WalkBackward(None).name: gameactions.ActionAndConfig(pa.WalkBackward, pa.WalkBackwardConfig()),
        pa.WalkLeft(None).name: gameactions.ActionAndConfig(pa.WalkLeft, pa.WalkLeftConfig()),
        pa.WalkRight(None).name: gameactions.ActionAndConfig(pa.WalkRight, pa.WalkRightConfig()),
        pa.SprintForward(None).name: gameactions.ActionAndConfig(pa.SprintForward, pa.SprintConfig()),
        pa.SprintBackward(None).name: gameactions.ActionAndConfig(pa.SprintBackward, pa.SprintConfig()),
        pa.SprintLeft(None).name: gameactions.ActionAndConfig(pa.SprintLeft, pa.SprintConfig()),
        pa.SprintRight(None).name: gameactions.ActionAndConfig(pa.SprintRight, pa.SprintConfig()),
        pa.CrouchToggle(None).name: gameactions.ActionAndConfig(pa.CrouchToggle, pa.CrouchToggleConfig()),
        pa.JournalToggle(None).name: gameactions.ActionAndConfig(pa.JournalToggle, pa.JournalToggleConfig()),
        pa.Place(None).name: gameactions.ActionAndConfig(pa.Place, pa.PlaceConfig()),
        pa.Pickup(None).name: gameactions.ActionAndConfig(pa.Pickup, pa.PickupConfig()),
        pa.Drop(None).name: gameactions.ActionAndConfig(pa.Drop, pa.DropConfig()),
        pa.Switch(None).name: gameactions.ActionAndConfig(pa.Switch, pa.SwitchConfig()),
        pa.TorchToggle(None).name: gameactions.ActionAndConfig(pa.TorchToggle, pa.TorchToggleConfig()),
        pa.Talk(None).name: gameactions.ActionAndConfig(pa.Talk, pa.TalkConfig()),
        pa.Radio(None).name: gameactions.ActionAndConfig(pa.Radio, pa.RadioConfig()),
        pa.LookUp(None).name: gameactions.ActionAndConfig(pa.LookUp, pa.LookUpConfig()),
        pa.LookDown(None).name: gameactions.ActionAndConfig(pa.LookDown, pa.LookDownConfig()),
        pa.LookLeft(None).name: gameactions.ActionAndConfig(pa.LookLeft, pa.LookLeftConfig()),
        pa.LookRight(None).name: gameactions.ActionAndConfig(pa.LookRight, pa.LookRightConfig()),
        pa.PeekUp(None).name: gameactions.ActionAndConfig(pa.PeekUp, pa.PeekUpConfig()),
        pa.PeekDown(None).name: gameactions.ActionAndConfig(pa.PeekDown, pa.PeekDownConfig()),
        pa.PeekLeft(None).name: gameactions.ActionAndConfig(pa.PeekLeft, pa.PeekLeftConfig()),
        pa.PeekRight(None).name: gameactions.ActionAndConfig(pa.PeekRight, pa.PeekRightConfig()),
        pa.Use(None).name: gameactions.ActionAndConfig(pa.Use, pa.UseConfig()),
        pa.combos.Box(None).name: gameactions.ActionAndConfig(pa.combos.Box, pa.combos.BoxConfig()),
        pa.combos.Teabag(None).name: gameactions.ActionAndConfig(pa.combos.Teabag, pa.combos.TeabagConfig()),
        pa.combos.Disco(None).name: gameactions.ActionAndConfig(pa.combos.Disco, pa.combos.DiscoConfig()),
        pa.combos.CycleItems(None).name: gameactions.ActionAndConfig(pa.combos.CycleItems, pa.combos.CycleItemsConfig()),
        pa.combos.CycleItemsAndUse(None).name: gameactions.ActionAndConfig(pa.combos.CycleItemsAndUse, pa.combos.CycleItemsAndUseConfig()),
        pa.combos.DropAllItems(None).name: gameactions.ActionAndConfig(pa.combos.DropAllItems, pa.combos.DropAllItemsConfig()),
        pa.combos.Spin(None).name: gameactions.ActionAndConfig(pa.combos.Spin, pa.combos.SpinConfig()),
        pa.combos.Headbang(None).name: gameactions.ActionAndConfig(pa.combos.Headbang, pa.combos.HeadbangConfig()),
        pa.combos.Headshake(None).name: gameactions.ActionAndConfig(pa.combos.Headshake, pa.combos.HeadshakeConfig()),
        pa.combos.Yoga(None).name: gameactions.ActionAndConfig(pa.combos.Yoga, pa.combos.YogaConfig()),
        pa.combos.Feet(None).name: gameactions.ActionAndConfig(pa.combos.Feet, pa.combos.FeetConfig()),
        pa.combos.Freeze(None).name: gameactions.ActionAndConfig(pa.combos.Freeze, pa.combos.FreezeConfig()),
        pa.combos.Tornado(None).name: gameactions.ActionAndConfig(pa.combos.Tornado, pa.combos.TornadoConfig()),
        pa.combos.Hurricane(None).name: gameactions.ActionAndConfig(pa.combos.Hurricane, pa.combos.HurricaneConfig()),
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
        pa.WalkForward(config_fn),
        pa.WalkBackward(config_fn),
        pa.WalkLeft(config_fn),
        pa.WalkRight(config_fn),
        pa.SprintForward(config_fn),
        pa.SprintBackward(config_fn),
        pa.SprintLeft(config_fn),
        pa.SprintRight(config_fn),
        pa.CrouchToggle(config_fn),
        pa.JournalToggle(config_fn),
        pa.Place(config_fn),
        pa.Pickup(config_fn),
        pa.Drop(config_fn),
        pa.Switch(config_fn),
        pa.TorchToggle(config_fn),
        pa.Talk(config_fn),
        pa.Radio(config_fn),
        pa.LookUp(config_fn),
        pa.LookDown(config_fn),
        pa.LookLeft(config_fn),
        pa.LookRight(config_fn),
        pa.PeekUp(config_fn),
        pa.PeekDown(config_fn),
        pa.PeekLeft(config_fn),
        pa.PeekRight(config_fn),
        pa.Use(config_fn),
        pa.combo.Box(config_fn),
        pa.combo.Teabag(config_fn),
        pa.combo.Disco(config_fn),
        pa.combo.CycleItems(config_fn),
        pa.combo.CycleItemsAndUse(config_fn),
        pa.combo.DropAllItems(config_fn),
        pa.combo.Spin(config_fn),
        pa.combo.Headbang(config_fn),
        pa.combo.Headshake(config_fn),
        pa.combo.Yoga(config_fn),
        pa.combo.Feet(config_fn),
        pa.combo.Freeze(config_fn),
        pa.combo.Tornado(config_fn),
        pa.combo.Hurricane(config_fn),
    ]


def all_actions_dict(config_fn: gameactions.ConfigFn) -> gameactions.ActionDict:
    """Get all actions as a dict"""
    return {action.name: action for action in all_actions(config_fn)}


def default_config() -> gameactions.Config:
    """Get the default config"""
    return gameactions.Config(
        {
            pa.WalkForward(None).name: pa.WalkForwardConfig(),
            pa.WalkBackward(None).name: pa.WalkBackwardConfig(),
            pa.WalkLeft(None).name: pa.WalkLeftConfig(),
            pa.WalkRight(None).name: pa.WalkRightConfig(),
            pa.SprintForward(None).name: pa.SprintConfig(),
            pa.SprintBackward(None).name: pa.SprintConfig(),
            pa.SprintLeft(None).name: pa.SprintConfig(),
            pa.SprintRight(None).name: pa.SprintConfig(),
            pa.CrouchToggle(None).name: pa.CrouchToggleConfig(),
            pa.JournalToggle(None).name: pa.JournalToggleConfig(),
            pa.Place(None).name: pa.PlaceConfig(),
            pa.Pickup(None).name: pa.PickupConfig(),
            pa.Drop(None).name: pa.DropConfig(),
            pa.Switch(None).name: pa.SwitchConfig(),
            pa.TorchToggle(None).name: pa.TorchToggleConfig(),
            pa.Talk(None).name: pa.TalkConfig(),
            pa.Radio(None).name: pa.RadioConfig(),
            pa.LookUp(None).name: pa.LookUpConfig(),
            pa.LookDown(None).name: pa.LookDownConfig(),
            pa.LookLeft(None).name: pa.LookLeftConfig(),
            pa.LookRight(None).name: pa.LookRightConfig(),
            pa.PeekUp(None).name: pa.PeekUpConfig(),
            pa.PeekDown(None).name: pa.PeekDownConfig(),
            pa.PeekLeft(None).name: pa.PeekLeftConfig(),
            pa.PeekRight(None).name: pa.PeekRightConfig(),
            pa.Use(None).name: pa.UseConfig(),
            pa.combo.Box(None).name: pa.combo.BoxConfig(),
            pa.combo.Teabag(None).name: pa.combo.TeabagConfig(),
            pa.combo.Disco(None).name: pa.combo.DiscoConfig(),
            pa.combo.CycleItems(None).name: pa.combo.CycleItemsConfig(),
            pa.combo.CycleItemsAndUse(None).name: pa.combo.CycleItemsAndUseConfig(),
            pa.combo.DropAllItems(None).name: pa.combo.DropAllItemsConfig(),
            pa.combo.Spin(None).name: pa.combo.SpinConfig(),
            pa.combo.Headbang(None).name: pa.combo.HeadbangConfig(),
            pa.combo.Headshake(None).name: pa.combo.HeadshakeConfig(),
            pa.combo.Yoga(None).name: pa.combo.YogaConfig(),
            pa.combo.Feet(None).name: pa.combo.FeetConfig(),
            pa.combo.Freeze(None).name: pa.combo.FreezeConfig(),
            pa.combo.Tornado(None).name: pa.combo.TornadoConfig(),
            pa.combo.Hurricane(None).name: pa.combo.HurricaneConfig(),
        }
    )
