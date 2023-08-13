#!./.venv/bin/python3
import dataclasses
import enum
import random
from typing import Any, Callable, Protocol

import actions
import errorcodes
import hidactions

DEBUG = False


@dataclasses.dataclass(slots=True)
class PhasmoActionConfig(Protocol):
    """A config for a Phasmophobia action"""
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

    @property
    def distance(self) -> int | None:
        """Get the distance"""
        ...


ConfigDict = dict[str, PhasmoActionConfig]


@dataclasses.dataclass(slots=True)
class Config:
    """The global config for all Phasmophobia actions"""
    config: dict[str, PhasmoActionConfig] = dataclasses.field(default_factory=dict)

    class Defaults:
        """Default values"""
        look_distance: int = 500
        peek_distance: int = 250
        toggle_duration: float = 0.1
        walk_duration: float = 3
        sprint_duration: float = 3
        sprint_key: str = "shift"
        talk_duration: float = 10

    def get_config(self, name: str) -> PhasmoActionConfig | None:
        """Look up an action config"""
        return self.config.get(name, None)


ConfigFn = Callable[[], Config]


@dataclasses.dataclass(slots=True, kw_only=True)
class PhasmoAction(hidactions.HidAction, Protocol):
    """Base class for Phasmophobia actions"""
    config_fn: ConfigFn
    name: str
    chained: bool

    @property
    def config(self) -> PhasmoActionConfig | None:
        """Get the config for this action"""
        ...


ActionDict = dict[str, PhasmoAction]


@dataclasses.dataclass(slots=True)
class GenericPhasmoActionBase:
    """Generic Phasmophobia action base class"""
    config_fn: ConfigFn

    @property
    def config(self) -> PhasmoActionConfig | None:
        """Get the config for this action"""
        return self.config_fn().get_config(self.name)  # TODO: think about relying on self.name existing in child class


@dataclasses.dataclass(slots=True)
class GenericPhasmoAction(GenericPhasmoActionBase):
    """Generic Phasmophobia action"""

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: PhasmoActionConfig = self.config

        if not actionconfig:
            return errorcodes.errorset(errorcodes.ErrorCode.LOOKUP_FAILURE)

        if isinstance(actionconfig.hidconfig, hidactions.KeyboardActionConfig):
            return hidactions.PressReleaseKey(actionconfig.hidconfig).run(force=force)
        elif isinstance(actionconfig.hidconfig, hidactions.MouseButtonActionConfig):
            return hidactions.PressReleaseButton(actionconfig.hidconfig).run(force=force)
        elif isinstance(actionconfig.hidconfig, hidactions.MouseMoveCartesianActionConfig):
            return hidactions.MoveMouseRelative(actionconfig.hidconfig).run(force=force)
        elif isinstance(actionconfig.hidconfig, hidactions.MouseMoveDirectionActionConfig):
            return hidactions.MoveMouseRelativeDirection(actionconfig.hidconfig).run(force=force)
        else:
            return errorcodes.errorset(errorcodes.ErrorCode.NOT_IMPLEMENTED)


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

    def to_action(self) -> "Walk":
        """Convert a walk direction to an action"""
        match self:
            case self.FORWARD:
                return WalkForward
            case self.BACKWARD:
                return WalkBackward
            case self.LEFT:
                return WalkLeft
            case self.RIGHT:
                return WalkRight
            case _:
                raise WalkDirectionUnknown(f"Unknown walk direction: {self}")


@dataclasses.dataclass(slots=True)
class Walk(GenericPhasmoAction):
    """Walk in a direction"""
    direction: WalkDirection
    name: str = dataclasses.field(init=False)
    chained: bool = False

    def __post_init__(self) -> None:
        self.name = self.direction.value

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: WalkConfig = self.config
        return hidactions.PressReleaseKey(actionconfig.hidconfig, actionconfig.duration).run(force=force)


@dataclasses.dataclass(slots=True)
class WalkConfig:
    hidconfig: hidactions.Config
    _duration: float = Config.Defaults.walk_duration

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class WalkForward(Walk):
    """Walk forward"""
    direction: WalkDirection = WalkDirection.FORWARD


@dataclasses.dataclass(slots=True)
class WalkForwardConfig(WalkConfig):
    """Walk forward config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("w"))


@dataclasses.dataclass(slots=True)
class WalkBackward(Walk):
    """Walk backward"""
    direction: WalkDirection = WalkDirection.BACKWARD


@dataclasses.dataclass(slots=True)
class WalkBackwardConfig(WalkConfig):
    """Walk backward config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("s"))


@dataclasses.dataclass(slots=True)
class WalkLeft(Walk):
    """Walk left"""
    direction: WalkDirection = WalkDirection.LEFT


@dataclasses.dataclass(slots=True)
class WalkLeftConfig(WalkConfig):
    """Walk left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("a"))


@dataclasses.dataclass(slots=True)
class WalkRight(Walk):
    """Walk right"""
    direction: WalkDirection = WalkDirection.RIGHT


@dataclasses.dataclass(slots=True)
class WalkRightConfig(WalkConfig):
    """Walk right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("d"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Sprint(Walk):
    """Sprint in a direction"""

    def __post_init__(self) -> None:
        self.name = "sprint_" + self.direction.value

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: SprintConfig = self.config

        return actions.ActionSequence([
            hidactions.PressKey(actionconfig.hidconfig),
            self.direction.to_action()(self.config_fn),
            hidactions.ReleaseKey(actionconfig.hidconfig),
        ]).run(force=force)


@dataclasses.dataclass(slots=True)
class SprintConfig:
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(Config.Defaults.sprint_key))
    _duration: float = Config.Defaults.sprint_duration

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class SprintForward(Sprint):
    """Sprint forward"""
    direction: WalkDirection = WalkDirection.FORWARD


@dataclasses.dataclass(slots=True)
class SprintBackward(Sprint):
    """Sprint backward"""
    direction: WalkDirection = WalkDirection.BACKWARD


@dataclasses.dataclass(slots=True)
class SprintLeft(Sprint):
    """Sprint left"""
    direction: WalkDirection = WalkDirection.LEFT


@dataclasses.dataclass(slots=True)
class SprintRight(Sprint):
    """Sprint right"""
    direction: WalkDirection = WalkDirection.RIGHT

#####################################################################


@dataclasses.dataclass(slots=True)
class CrouchToggle(GenericPhasmoAction):
    """Toggle crouch"""
    name: str = "crouch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class CrouchToggleConfig:
    """Toggle crouch config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("c"))


#####################################################################


@dataclasses.dataclass(slots=True)
class JournalToggle(GenericPhasmoAction):
    """Toggle the journal"""
    name: str = "journal"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class JournalToggleConfig:
    """Toggle the journal config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("j"))


#####################################################################


@dataclasses.dataclass(slots=True)
class Place(GenericPhasmoAction):
    """Place an item"""
    name: str = "place"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PlaceConfig:
    """Place an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("f"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Pickup(GenericPhasmoAction):
    """Pickup an item"""
    name: str = "pickup"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PickupConfig:
    """Pickup an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("e"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Drop(GenericPhasmoAction):
    """Drop an item"""
    name: str = "drop"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class DropConfig:
    """Drop an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("g"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Switch(GenericPhasmoAction):
    """Switch to next inventory item"""
    name: str = "switch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class SwitchConfig:
    """Switch to next inventory item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("q"))

#####################################################################


@dataclasses.dataclass(slots=True)
class TorchToggle(GenericPhasmoAction):
    """Toggle the torch"""
    name: str = "torch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TorchToggleConfig:
    """Toggle the torch config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("t"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Talk(GenericPhasmoAction):
    """Toggle push to talk for a period of time"""
    name: str = "talk"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TalkConfig:
    """Toggle push to talk for a period of time config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("v"))
    _duration: float = Config.Defaults.talk_duration

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration

#####################################################################


@dataclasses.dataclass(slots=True)
class LookConfig:
    hidconfig: hidactions.Config


@dataclasses.dataclass(slots=True)
class LookUp(GenericPhasmoAction):
    """Look up"""
    name: str = "look_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookUpConfig(LookConfig):
    """Look up config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.look_distance, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class LookDown(GenericPhasmoAction):
    """Look down"""
    name: str = "look_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookDownConfig(LookConfig):
    """Look down config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.look_distance, hidactions.MouseMoveDirection.DOWN))


@dataclasses.dataclass(slots=True)
class LookLeft(GenericPhasmoAction):
    """Look left"""
    name: str = "look_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookLeftConfig(LookConfig):
    """Look left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.look_distance, hidactions.MouseMoveDirection.LEFT))


@dataclasses.dataclass(slots=True)
class LookRight(GenericPhasmoAction):
    """Look right"""
    name: str = "look_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookRightConfig(LookConfig):
    """Look right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.look_distance, hidactions.MouseMoveDirection.RIGHT))


PeekConfig = LookConfig


@dataclasses.dataclass(slots=True)
class PeekUp(GenericPhasmoAction):
    """Peek up"""
    name: str = "peek_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekUpConfig(PeekConfig):
    """Peek up config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.peek_distance, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class PeekDown(GenericPhasmoAction):
    """Peek down"""
    name: str = "peek_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekDownConfig(PeekConfig):
    """Peek down config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.peek_distance, hidactions.MouseMoveDirection.DOWN))


@dataclasses.dataclass(slots=True)
class PeekLeft(GenericPhasmoAction):
    """Peek left"""
    name: str = "peek_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekLeftConfig(PeekConfig):
    """Peek left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.peek_distance, hidactions.MouseMoveDirection.LEFT))


@dataclasses.dataclass(slots=True)
class PeekRight(GenericPhasmoAction):
    """Peek right"""
    name: str = "peek_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekRightConfig(PeekConfig):
    """Peek right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionActionConfig(Config.Defaults.peek_distance, hidactions.MouseMoveDirection.RIGHT))

#####################################################################


@dataclasses.dataclass(slots=True)
class Use(GenericPhasmoAction):
    """Use item"""
    name: str = "use"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class UseConfig:
    """Use item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseButtonActionConfig("right"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Box(GenericPhasmoAction):
    """Music box grenade; use and drop"""
    name: str = "box"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: BoxConfig = self.config
        return actions.ActionSequence([Use(self.config_fn), actions.Wait(actionconfig.pause), Drop(self.config_fn)]).run(force=force)


@dataclasses.dataclass(slots=True)
class BoxConfig:
    """Use item config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.5

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

#####################################################################


@dataclasses.dataclass(slots=True)
class Teabag(GenericPhasmoActionBase):
    """Crouch repeatedly"""
    name: str = "teabag"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: TeabagConfig = self.config
        return actions.ActionRepeatWithWait(CrouchToggle(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class TeabagConfig:
    """Crouch repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.5
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))

    def __post_init__(self) -> None:
        if not isinstance(self._repeats, tuple):
            self._repeats = tuple(self._repeats)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return random.randint(*self._repeats)

#####################################################################


@dataclasses.dataclass(slots=True)
class Disco(GenericPhasmoActionBase):
    """Turn the torch on and off repeatedly"""
    name: str = "disco"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: DiscoConfig = self.config
        return actions.ActionRepeatWithWait(TorchToggle(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class DiscoConfig:
    """Turn the torch on and off repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.33
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))

    def __post_init__(self) -> None:
        if not isinstance(self._repeats, tuple):
            self._repeats = tuple(self._repeats)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return random.randint(*self._repeats)

#####################################################################


@dataclasses.dataclass(slots=True)
class CycleItems(GenericPhasmoActionBase):
    """Cycle through the inventory repeatedly"""
    name: str = "cycle"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: CycleItemsConfig = self.config
        return actions.ActionRepeatWithWait(Switch(self.config_fn), actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class CycleItemsConfig:
    """Cycle through the inventory repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.25
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))

    def __post_init__(self) -> None:
        if not isinstance(self._repeats, tuple):
            self._repeats = tuple(self._repeats)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return random.randint(*self._repeats)

#####################################################################


@dataclasses.dataclass(slots=True)
class CycleItemsAndUse(GenericPhasmoActionBase):
    """Cycle through the inventory and use the item, repeatedly"""
    name: str = "rekt"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: CycleItemsAndUseConfig = self.config
        sequence = actions.ActionSequence([Switch(self.config_fn), actions.Wait(actionconfig.pause), Use(self.config_fn)])
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

#####################################################################


@dataclasses.dataclass(slots=True)
class DropAllItems(GenericPhasmoActionBase):
    """Cycle through the inventory and drop each item"""
    name: str = "yeet"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: DropAllItemsConfig = self.config
        sequence = actions.ActionSequence([Drop(self.config_fn), actions.Wait(actionconfig.pause), Switch(self.config_fn)])
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

#####################################################################


@dataclasses.dataclass(slots=True)
class Spin(GenericPhasmoActionBase):
    """Spin on the spot"""
    name: str = "spin"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: SpinConfig = self.config

        direction = actionconfig.mousemovedirection or hidactions.MouseMoveDirection.RIGHT
        distance = actionconfig.distance or (LookRight().config.hidconfig.distance // 5)

        look_action = hidactions.MoveMouseRelativeDirection(hidactions.MouseMoveDirectionActionConfig(distance, direction))
        return actions.ActionRepeatWithWait(look_action, actionconfig.repeats, actions.Wait(actionconfig.pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class SpinConfig:
    """Spin on the spot config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.015
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (25, 50))
    _mousemovedirection: hidactions.MouseMoveDirection = None
    _distance: int = Config.Defaults.look_distance // 5

    def __post_init__(self) -> None:
        if not isinstance(self._repeats, tuple):
            self._repeats = tuple(self._repeats)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return random.randint(*self._repeats)

    @property
    def mousemovedirection(self) -> hidactions.MouseMoveDirection:
        """Get the mouse move direction"""
        return self._mousemovedirection or random.choice(list([hidactions.MouseMoveDirection.RIGHT, hidactions.MouseMoveDirection.LEFT]))

    @property
    def distance(self) -> int:
        """Get the distance"""
        return self._distance

#####################################################################


@dataclasses.dataclass(slots=True)
class Headbang(GenericPhasmoActionBase):
    """Look up and down repeatedly"""
    name: str = "headbang"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: HeadbangConfig = self.config
        repeats = actionconfig.repeats
        pause = actionconfig.pause

        if DEBUG:
            print(f"Headbang: repeats={repeats}, pause={pause}")

        distance = actionconfig.distance or Config.Defaults.peek_distance

        lookup = hidactions.MoveMouseRelativeDirection(hidactions.MouseMoveDirectionActionConfig(distance, hidactions.MouseMoveDirection.UP))
        lookdown = hidactions.MoveMouseRelativeDirection(hidactions.MouseMoveDirectionActionConfig(distance, hidactions.MouseMoveDirection.DOWN))

        once = actions.ActionSequence([lookup, actions.Wait(pause), lookdown])
        return actions.ActionRepeatWithWait(once, repeats, actions.Wait(pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class HeadbangConfig:
    """Look up and down repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.33
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))
    _distance: int = Config.Defaults.peek_distance

    def __post_init__(self) -> None:
        if not isinstance(self._repeats, tuple):
            self._repeats = tuple(self._repeats)

    @property
    def pause(self) -> float:
        """Get the pause"""
        return self._pause

    @property
    def repeats(self) -> int:
        """Get the repeats"""
        return random.randint(*self._repeats)

    @property
    def distance(self) -> int:
        """Get the distance"""
        return self._distance

#####################################################################


@dataclasses.dataclass(slots=True)
class RandomAction(GenericPhasmoActionBase):
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
    _actiondict: Callable[[], ActionDict]
    hidconfig: hidactions.Config = None

    @property
    def actiondict(self) -> ActionDict:
        """Get the action dictionary"""
        return self._actiondict()


#####################################################################

def all_actions(config_fn: ConfigFn) -> list[PhasmoAction]:
    """Get all actions"""
    return [
        WalkForward(config_fn),
        WalkBackward(config_fn),
        WalkLeft(config_fn),
        WalkRight(config_fn),
        SprintForward(config_fn),
        SprintBackward(config_fn),
        SprintLeft(config_fn),
        SprintRight(config_fn),
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
        Box(config_fn),
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


def all_actions_dict(config_fn: ConfigFn) -> ActionDict:
    """Get all actions as a dict"""
    return {action.name: action for action in all_actions(config_fn)}


def default_config() -> Config:
    """Get the default config"""
    return Config({
        WalkForward(None).name: WalkForwardConfig(),
        WalkBackward(None).name: WalkBackwardConfig(),
        WalkLeft(None).name: WalkLeftConfig(),
        WalkRight(None).name: WalkRightConfig(),
        SprintForward(None).name: SprintConfig(),
        SprintBackward(None).name: SprintConfig(),
        SprintLeft(None).name: SprintConfig(),
        SprintRight(None).name: SprintConfig(),
        CrouchToggle(None).name: CrouchToggleConfig(),
        JournalToggle(None).name: JournalToggleConfig(),
        Place(None).name: PlaceConfig(),
        Pickup(None).name: PickupConfig(),
        Drop(None).name: DropConfig(),
        Switch(None).name: SwitchConfig(),
        TorchToggle(None).name: TorchToggleConfig(),
        Talk(None).name: TalkConfig(),
        LookUp(None).name: LookUpConfig(),
        LookDown(None).name: LookDownConfig(),
        LookLeft(None).name: LookLeftConfig(),
        LookRight(None).name: LookRightConfig(),
        PeekUp(None).name: PeekUpConfig(),
        PeekDown(None).name: PeekDownConfig(),
        PeekLeft(None).name: PeekLeftConfig(),
        PeekRight(None).name: PeekRightConfig(),
        Use(None).name: UseConfig(),
        Box(None).name: BoxConfig(),
        Teabag(None).name: TeabagConfig(),
        Disco(None).name: DiscoConfig(),
        CycleItems(None).name: CycleItemsConfig(),
        CycleItemsAndUse(None).name: CycleItemsAndUseConfig(),
        DropAllItems(None).name: DropAllItemsConfig(),
        Spin(None).name: SpinConfig(),
        Headbang(None).name: HeadbangConfig(),
    })


def from_toml(existing: dict[str, dict[str, Any]]) -> Config:
    """Get a config from an existing config"""
    ret = default_config()
    for key in ret.config.keys():
        if key in existing:
            to_replace = ret.config[key]
            using_this = existing.get(key, None)
            if using_this:
                to_replace_hidconfig = to_replace.hidconfig
                using_this_hidconfig = using_this.get("hidconfig", None)
                kwargs = {**using_this}
                if to_replace_hidconfig:
                    kwargs["hidconfig"] = type(to_replace.hidconfig)(**using_this_hidconfig) if using_this_hidconfig else to_replace.hidconfig
                    kwargs["hidconfig"].device = hidactions.HidType[kwargs["hidconfig"].device]
                else:
                    kwargs["hidconfig"] = None
                ret.config[key] = type(to_replace)(**kwargs)
    return ret


if __name__ == "__main__":
    import pprint as pp
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

    myactions["look_up"].run(force=force)
    myactions["look_down"].run(force=force)
    myactions["headbang"].run(force=force)
