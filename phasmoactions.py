#!./.venv/bin/python3
import dataclasses
import enum
from typing import Any, Callable, Protocol

import actions
import hidactions

DEBUG = True


@dataclasses.dataclass(slots=True)
class PhasmoActionConfig(Protocol):
    """A config to a Phasmophobia action"""
    hidconfig: hidactions.Config

    @property
    def duration(self) -> float | None:
        """Get the duration"""
        ...

    @property
    def pause(self) -> float | None:
        """Get the pause"""
        ...

    @property
    def repeats(self) -> int | None:
        """Get the repeats"""
        ...

    @property
    def mousemovedirection(self) -> hidactions.MouseMoveDirection | None:
        """Get the mouse move direction"""
        ...


@dataclasses.dataclass(slots=True)
class Config:
    config: dict[str, PhasmoActionConfig] = dataclasses.field(default_factory=dict)

    class Defaults:
        """Default values"""
        look_distance: int = 500
        peek_distance: int = 250
        toggle_duration: float = 0.1
        walk_duration: float = 3
        talk_duration: float = 10

    class ConfigLookupFailure(Exception):
        pass

    def get_config(self, name: str) -> PhasmoActionConfig | None:
        """Look up an action config"""
        return self.config.get(name, None)

    def __getitem__(self, name: str) -> PhasmoActionConfig:
        """Look up an action config"""
        try:
            return self.config[name]
        except KeyError:
            raise self.ConfigLookupFailure(f"Config {name} not found")


@dataclasses.dataclass(slots=True, kw_only=True)
class PhasmoAction(hidactions.HidAction, Protocol):
    """Base class for Phasmophobia actions"""
    config_fn: Callable[[], Config]
    name: str
    chained: bool

    @property
    def config(self) -> PhasmoActionConfig | None:
        """Get the config for this action"""
        ...


@dataclasses.dataclass(slots=True)
class GenericPhasmoActionBase:
    """Generic Phasmophobia action base class"""
    config_fn: Callable[[], Config]

    @property
    def config(self) -> PhasmoActionConfig | None:
        """Get the config for this action"""
        return self.config_fn().get_config(self.name)  # TODO: think about relying on self.name existing in child class


@dataclasses.dataclass(slots=True)
class GenericPhasmoAction(GenericPhasmoActionBase):
    """Generic Phasmophobia action"""

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config

        if isinstance(actionconfig.hidconfig, hidactions.KeyboardActionConfig):
            hidactions.PressReleaseKey(actionconfig.hidconfig).run()
        elif isinstance(actionconfig.hidconfig, hidactions.MouseButtonActionConfig):
            hidactions.PressReleaseButton(actionconfig.hidconfig).run()
        elif isinstance(actionconfig.hidconfig, hidactions.MouseMoveCartesianActionConfig):
            hidactions.MoveMouseRelative(actionconfig.hidconfig).run()
        elif isinstance(actionconfig.hidconfig, hidactions.MouseMoveDirectionActionConfig):
            hidactions.MoveMouseRelativeDirection(actionconfig.hidconfig).run()
        else:
            raise NotImplementedError(f"Unknown action config: {actionconfig}")


#####################################################################


class WalkDirectionUnknown(Exception):
    """Unknown walk direction"""
    pass


@enum.unique
class WalkDirection(enum.Enum):
    """Walk direction"""
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"

    def _missing_(self, value: Any) -> Any:
        """Handle missing values"""
        raise self.WalkDirectionUnknown(f"Unknown walk direction: {value}")


@dataclasses.dataclass(slots=True)
class Walk(GenericPhasmoAction):
    """Walk in a direction"""
    direction: WalkDirection
    name: str = dataclasses.field(init=False)
    chained: bool = False

    def __post_init__(self) -> None:
        self.name = self.direction.value


@dataclasses.dataclass(slots=True)
class WalkForward(Walk):
    """Walk forward"""
    direction: WalkDirection = WalkDirection.FORWARD


@dataclasses.dataclass(slots=True)
class WalkBackward(Walk):
    """Walk backward"""
    direction: WalkDirection = WalkDirection.BACKWARD


@dataclasses.dataclass(slots=True)
class WalkLeft(Walk):
    """Walk left"""
    direction: WalkDirection = WalkDirection.LEFT


@dataclasses.dataclass(slots=True)
class WalkRight(Walk):
    """Walk right"""
    direction: WalkDirection = WalkDirection.RIGHT

#####################################################################


@dataclasses.dataclass(slots=True)
class CrouchToggle(GenericPhasmoAction):
    """Toggle crouch"""
    name: str = "crouch"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class JournalToggle(GenericPhasmoAction):
    """Toggle the journal"""
    name: str = "journal"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class Place(GenericPhasmoAction):
    """Place an item"""
    name: str = "place"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class Pickup(GenericPhasmoAction):
    """Pickup an item"""
    name: str = "pickup"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class Drop(GenericPhasmoAction):
    """Drop an item"""
    name: str = "Drop"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class Switch(GenericPhasmoAction):
    """Switch to next inventory item"""
    name: str = "switch"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class TorchToggle(GenericPhasmoAction):
    """Toggle the torch"""
    name: str = "torch"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class Talk(GenericPhasmoAction):
    """Toggle push to talk for a period of time"""
    name: str = "talk"
    chained: bool = False


#####################################################################


@dataclasses.dataclass(slots=True)
class LookUp(GenericPhasmoAction):
    """Look up"""
    name: str = "look_up"


@dataclasses.dataclass(slots=True)
class LookDown(GenericPhasmoAction):
    """Look down"""
    name: str = "look_down"


@dataclasses.dataclass(slots=True)
class LookLeft(GenericPhasmoAction):
    """Look left"""
    name: str = "look_left"


@dataclasses.dataclass(slots=True)
class LookRight(GenericPhasmoAction):
    """Look right"""
    name: str = "look_right"


@dataclasses.dataclass(slots=True)
class PeekUp(GenericPhasmoAction):
    """Peek up"""
    name: str = "peek_up"


@dataclasses.dataclass(slots=True)
class PeekDown(GenericPhasmoAction):
    """Peek down"""
    name: str = "peek_down"


@dataclasses.dataclass(slots=True)
class PeekLeft(GenericPhasmoAction):
    """Peek left"""
    name: str = "peek_left"


@dataclasses.dataclass(slots=True)
class PeekRight(GenericPhasmoAction):
    """Peek right"""
    name: str = "peek_right"

#####################################################################


@dataclasses.dataclass(slots=True)
class Use(GenericPhasmoAction):
    """Use item"""
    name: str = "use"
    chained: bool = False


#####################################################################

@dataclasses.dataclass(slots=True)
class Teabag(GenericPhasmoActionBase):
    """Crouch repeatedly"""
    name: str = "teabag"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config
        actions.ActionRepeatWithWait(CrouchToggle(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run()

#####################################################################


@dataclasses.dataclass(slots=True)
class Disco(GenericPhasmoActionBase):
    """Turn the torch on and off repeatedly"""
    name: str = "disco"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config
        actions.ActionRepeatWithWait(TorchToggle(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run()

#####################################################################


@dataclasses.dataclass(slots=True)
class CycleItems(GenericPhasmoActionBase):
    """Cycle through the inventory repeatedly"""
    name: str = "cycle"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config
        actions.ActionRepeatWithWait(Switch(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run()

#####################################################################


@dataclasses.dataclass(slots=True)
class CycleItemsAndUse(GenericPhasmoActionBase):
    """Cycle through the inventory and use the item, repeatedly"""
    name: str = "cycle_items_and_use"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config
        sequence = actions.ActionSequence([Switch(self.config_fn), actions.Wait(actionconfig.pause), Use(self.config_fn)])
        actions.ActionRepeatWithWait(sequence, actionconfig.repeats, actions.Wait(actionconfig.pause)).run()

#####################################################################


@dataclasses.dataclass(slots=True)
class DropAllItems(GenericPhasmoActionBase):
    """Cycle through the inventory and drop each item"""
    name: str = "drop_all_items"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config
        sequence = actions.ActionSequence([Switch(self.config_fn), actions.Wait(actionconfig.pause), Drop(self.config_fn)])
        actions.ActionRepeatWithWait(sequence, actionconfig.repeats, actions.Wait(actionconfig.pause)).run()

#####################################################################


@dataclasses.dataclass(slots=True)
class Spin(GenericPhasmoActionBase):
    """Cycle through the inventory and drop each item"""
    name: str = "spin"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config

        direction = actionconfig.mousemovedirection or hidactions.MouseMoveDirection.RIGHT
        distance = actionconfig.distance or LookRight().config.hidconfig.distance

        look_action = hidactions.MoveMouseRelativeDirection(distance, direction)
        actions.ActionRepeatWithWait(look_action, actionconfig.repeats, actions.Wait(actionconfig.pause)).run()

#####################################################################


@dataclasses.dataclass(slots=True)
class Headbang(GenericPhasmoActionBase):
    """Look up and down repeatedly"""
    name: str = "headbang"
    chained: bool = True

    def run(self) -> None:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config
        repeats = actionconfig.repeats
        pause = actionconfig.pause

        if DEBUG:
            print(f"Headbang: repeats={repeats}, pause={pause}")

        look_up = LookUp(self.config_fn)
        look_down = LookDown(self.config_fn)

        once = actions.ActionSequence([LookUp(self.config_fn), actions.Wait(pause), LookDown(self.config_fn)])
        actions.ActionRepeatWithWait(once, repeats, actions.Wait(pause)).run()

#####################################################################


def all_actions(config_fn: Callable[[], Config]) -> list[PhasmoAction]:
    """Get all actions"""
    return [
        WalkForward(config_fn),
        WalkBackward(config_fn),
        WalkLeft(config_fn),
        WalkRight(config_fn),
        CrouchToggle(config_fn),
        JournalToggle(config_fn),
        Place(config_fn),
        Pickup(config_fn),
        Drop(config_fn),
        Switch(config_fn),
        TorchToggle(config_fn),
        Talk(config_fn),
        LookUp(config_fn),
        LookDown(config_fn),
        LookLeft(config_fn),
        LookRight(config_fn),
        PeekUp(config_fn),
        PeekDown(config_fn),
        PeekLeft(config_fn),
        PeekRight(config_fn),
        Use(config_fn),
        Teabag(config_fn),
        Disco(config_fn),
        CycleItems(config_fn),
        CycleItemsAndUse(config_fn),
        DropAllItems(config_fn),
        Spin(config_fn),
        Headbang(config_fn),
    ]


def get_default_action_names() -> list[str]:
    """Get the default action names"""
    return [action.name for action in all_actions(Config())]


def all_actions_dict(config_fn: Callable[[], Config]) -> dict[str, PhasmoAction]:
    """Get all actions as a dict"""
    return {action.name: action for action in all_actions(config_fn)}


if __name__ == "__main__":
    import pprint as pp
    import random
    pp.pprint(get_default_action_names())
    pp.pprint(all_actions_dict(Config()))

    @dataclasses.dataclass(slots=True)
    class LookActionConfig:
        hidconfig: hidactions.Config

    look_up_hidconfig = hidactions.MouseMoveDirectionActionConfig(500, hidactions.MouseMoveDirection.UP)
    look_up_config = LookActionConfig(hidconfig=look_up_hidconfig)
    look_down_hidconfig = hidactions.MouseMoveDirectionActionConfig(250, hidactions.MouseMoveDirection.DOWN)
    look_down_config = LookActionConfig(hidconfig=look_down_hidconfig)

    config = Config(config={
        "look_up": look_up_config,
        "look_down": look_down_config,
    })

    pp.pprint(all_actions_dict(lambda: config))

    @dataclasses.dataclass(slots=True)
    class HeadbangActionConfig:
        hidconfig: hidactions.Config = None
        _pause: float = 0.1
        _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (3, 10))

        @property
        def pause(self) -> float | None:
            """Get the pause"""
            return self._pause

        @property
        def repeats(self) -> int | None:
            """Get the repeats"""
            return random.randint(*self._repeats)

    config.config["headbang"] = HeadbangActionConfig()

    myactions = all_actions_dict(lambda: config)

    myactions["look_up"].run()
    myactions["look_down"].run()
    myactions["headbang"].run()
