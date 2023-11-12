#!./.venv/bin/python3
import dataclasses
import enum
import random
from typing import Any, Callable, ClassVar

from . import actions, environment, errorcodes, gameactions, hidactions

DEBUG = environment.getenvboolean("DEBUG", False)

GenericActionBase = gameactions.GenericActionBase
GenericAction = gameactions.GenericAction


@dataclasses.dataclass(slots=True, frozen=True)
class DEFAULTS:
    """Default values for Phasmophobia actions"""
    LOOK_DISTANCE: ClassVar[int] = 500
    PEEK_DISTANCE: ClassVar[int] = 250
    TOGGLE_DURATION: ClassVar[float] = 0.1
    WALK_DURATION: ClassVar[float] = 3
    SPRINT_DURATION: ClassVar[float] = 3
    TALK_DURATION: ClassVar[float] = 10

    @dataclasses.dataclass(slots=True, frozen=True)
    class KEYBINDS:
        """Default Phasmophobia keybinds"""
        FORWARD: ClassVar[str] = "w"
        BACKWARD: ClassVar[str] = "s"
        LEFT: ClassVar[str] = "a"
        RIGHT: ClassVar[str] = "d"
        USE: ClassVar[str] = "right"
        INTERACT: ClassVar[str] = "left"
        PICKUP: ClassVar[str] = "e"
        PLACE: ClassVar[str] = "f"
        DROP: ClassVar[str] = "g"
        TORCH: ClassVar[str] = "t"
        SWITCH: ClassVar[str] = "q"
        CROUCH: ClassVar[str] = "c"
        SPRINT: ClassVar[str] = "shift_l"
        JOURNAL: ClassVar[str] = "j"
        TALK: ClassVar[str] = "v"
        RADIO: ClassVar[str] = "b"


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
class Walk(GenericAction):
    """Walk in a direction"""
    direction: WalkDirection
    name: str = dataclasses.field(init=False)
    chained: bool = False

    def __post_init__(self) -> None:
        self.name = self.direction.value

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: WalkConfig = self.config
        return hidactions.PressReleaseKeyOrButton(actionconfig.hidconfig, actionconfig.duration).run(force=force)


@dataclasses.dataclass(slots=True)
class WalkConfig:
    hidconfig: hidactions.Config
    _duration: float = DEFAULTS.WALK_DURATION

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
            hidactions.PressKeyOrButton(actionconfig.hidconfig),
            self.direction.to_action()(self.config_fn),
            hidactions.ReleaseKeyOrButton(actionconfig.hidconfig),
        ]).run(force=force)


@dataclasses.dataclass(slots=True)
class SprintConfig:
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig(DEFAULTS.KEYBINDS.SPRINT))
    _duration: float = DEFAULTS.SPRINT_DURATION

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
class CrouchToggle(GenericAction):
    """Toggle crouch"""
    name: str = "crouch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class CrouchToggleConfig:
    """Toggle crouch config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("c"))


#####################################################################


@dataclasses.dataclass(slots=True)
class JournalToggle(GenericAction):
    """Toggle the journal"""
    name: str = "journal"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class JournalToggleConfig:
    """Toggle the journal config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("j"))


#####################################################################


@dataclasses.dataclass(slots=True)
class Place(GenericAction):
    """Place an item"""
    name: str = "place"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PlaceConfig:
    """Place an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("f"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Pickup(GenericAction):
    """Pickup an item"""
    name: str = "pickup"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PickupConfig:
    """Pickup an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("e"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Drop(GenericAction):
    """Drop an item"""
    name: str = "drop"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class DropConfig:
    """Drop an item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("g"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Switch(GenericAction):
    """Switch to next inventory item"""
    name: str = "switch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class SwitchConfig:
    """Switch to next inventory item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("q"))

#####################################################################


@dataclasses.dataclass(slots=True)
class TorchToggle(GenericAction):
    """Toggle the torch"""
    name: str = "torch"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TorchToggleConfig:
    """Toggle the torch config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("t"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Talk(GenericAction):
    """Toggle push to talk for a period of time"""
    name: str = "talk"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class TalkConfig:
    """Toggle push to talk for a period of time config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("v"))
    _duration: float = DEFAULTS.TALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


@dataclasses.dataclass(slots=True)
class Radio(GenericAction):
    """Toggle global push to talk radio for a period of time"""
    name: str = "radio"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class RadioConfig:
    """Toggle global push to talk radio for a period of time config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("b"))
    _duration: float = DEFAULTS.TALK_DURATION

    @property
    def duration(self) -> float:
        """Get the duration"""
        return self._duration


#####################################################################


@dataclasses.dataclass(slots=True)
class LookConfig:
    hidconfig: hidactions.Config


@dataclasses.dataclass(slots=True)
class LookUp(GenericAction):
    """Look up"""
    name: str = "look_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookUpConfig(LookConfig):
    """Look up config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class LookDown(GenericAction):
    """Look down"""
    name: str = "look_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookDownConfig(LookConfig):
    """Look down config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.DOWN))


@dataclasses.dataclass(slots=True)
class LookLeft(GenericAction):
    """Look left"""
    name: str = "look_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookLeftConfig(LookConfig):
    """Look left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.LEFT))


@dataclasses.dataclass(slots=True)
class LookRight(GenericAction):
    """Look right"""
    name: str = "look_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class LookRightConfig(LookConfig):
    """Look right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.LOOK_DISTANCE, hidactions.MouseMoveDirection.RIGHT))


PeekConfig = LookConfig


@dataclasses.dataclass(slots=True)
class PeekUp(GenericAction):
    """Peek up"""
    name: str = "peek_up"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekUpConfig(PeekConfig):
    """Peek up config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.UP))


@dataclasses.dataclass(slots=True)
class PeekDown(GenericAction):
    """Peek down"""
    name: str = "peek_down"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekDownConfig(PeekConfig):
    """Peek down config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.DOWN))


@dataclasses.dataclass(slots=True)
class PeekLeft(GenericAction):
    """Peek left"""
    name: str = "peek_left"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekLeftConfig(PeekConfig):
    """Peek left config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.LEFT))


@dataclasses.dataclass(slots=True)
class PeekRight(GenericAction):
    """Peek right"""
    name: str = "peek_right"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class PeekRightConfig(PeekConfig):
    """Peek right config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(DEFAULTS.PEEK_DISTANCE, hidactions.MouseMoveDirection.RIGHT))

#####################################################################


@dataclasses.dataclass(slots=True)
class Use(GenericAction):
    """Use item"""
    name: str = "use"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class UseConfig:
    """Use item config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseButtonActionConfig("right"))

#####################################################################


@dataclasses.dataclass(slots=True)
class Box(GenericAction):
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
class Teabag(GenericActionBase):
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
class Disco(GenericActionBase):
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
class CycleItems(GenericActionBase):
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
class CycleItemsAndUse(GenericActionBase):
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
class DropAllItems(GenericActionBase):
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
class Spin(GenericActionBase):
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
    _distance: int = DEFAULTS.LOOK_DISTANCE // 5

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
class Headbang(GenericActionBase):
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

        distance = actionconfig.distance or DEFAULTS.PEEK_DISTANCE

        lookup = hidactions.MoveMouseRelativeDirectionSmooth(hidactions.MouseMoveDirectionSmoothActionConfig(distance, hidactions.MouseMoveDirection.UP))
        lookdown = hidactions.MoveMouseRelativeDirectionSmooth(hidactions.MouseMoveDirectionSmoothActionConfig(distance, hidactions.MouseMoveDirection.DOWN))

        once = actions.ActionSequence([lookup, actions.Wait(pause), lookdown])
        return actions.ActionRepeatWithWait(once, repeats, actions.Wait(pause)).run(force=force)


@dataclasses.dataclass(slots=True)
class HeadbangConfig:
    """Look up and down repeatedly config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.33
    _repeats: tuple[int] = dataclasses.field(default_factory=lambda: (5, 10))
    _distance: int = DEFAULTS.PEEK_DISTANCE

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
class Yoga(GenericAction):
    """Look up to the sky"""
    name: str = "yoga"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class YogaConfig(LookConfig):
    """Look up to the sky config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(4096, hidactions.MouseMoveDirection.UP))

#####################################################################


@dataclasses.dataclass(slots=True)
class Feet(GenericAction):
    """Look down to the floor"""
    name: str = "feet"
    chained: bool = False


@dataclasses.dataclass(slots=True)
class FeetConfig(LookConfig):
    """Look down to the floor config"""
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.MouseMoveDirectionSmoothActionConfig(4096, hidactions.MouseMoveDirection.DOWN))

#####################################################################


@dataclasses.dataclass(slots=True)
class Freeze(GenericActionBase):
    """Counterstrafe to freeze on the spot"""
    name: str = "freeze"
    chained: bool = True

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: FreezeConfig = self.config

        forwardPress = hidactions.PressKeyOrButton(WalkForwardConfig().hidconfig)
        rightPress = hidactions.PressKeyOrButton(WalkRightConfig().hidconfig)
        backwardPress = hidactions.PressKeyOrButton(WalkBackwardConfig().hidconfig)
        leftPress = hidactions.PressKeyOrButton(WalkLeftConfig().hidconfig)

        press = actions.ActionSequence([forwardPress,
                                        rightPress,
                                        backwardPress,
                                        leftPress])

        forwardRelease = hidactions.ReleaseKeyOrButton(WalkForwardConfig().hidconfig)
        rightRelease = hidactions.ReleaseKeyOrButton(WalkRightConfig().hidconfig)
        backwardRelease = hidactions.ReleaseKeyOrButton(WalkBackwardConfig().hidconfig)
        leftRelease = hidactions.ReleaseKeyOrButton(WalkLeftConfig().hidconfig)

        release = actions.ActionSequence([forwardRelease,
                                          rightRelease,
                                          backwardRelease,
                                          leftRelease])

        once = actions.ActionSequence([press, actions.Wait(actionconfig.pause), release, actions.Wait(actionconfig.pause)])

        return actions.ActionRepeat(once, actionconfig.repeats).run(force=force)


@dataclasses.dataclass(slots=True)
class FreezeConfig:
    """Counterstrafe to freeze on the spot config"""
    hidconfig: hidactions.Config = None
    _pause: float = 0.01
    _repeats: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self._repeats = int(5.0 / 4.0 / self._pause)

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

def _get_all(config_fn: gameactions.ConfigFn) -> gameactions.ActionAndConfigDict:
    return {
        WalkForward(None).name: gameactions.ActionAndConfig(WalkForward, WalkForwardConfig()),
        WalkBackward(None).name: gameactions.ActionAndConfig(WalkBackward, WalkBackwardConfig()),
        WalkLeft(None).name: gameactions.ActionAndConfig(WalkLeft, WalkLeftConfig()),
        WalkRight(None).name: gameactions.ActionAndConfig(WalkRight, WalkRightConfig()),
        SprintForward(None).name: gameactions.ActionAndConfig(SprintForward, SprintConfig()),
        SprintBackward(None).name: gameactions.ActionAndConfig(SprintBackward, SprintConfig()),
        SprintLeft(None).name: gameactions.ActionAndConfig(SprintLeft, SprintConfig()),
        SprintRight(None).name: gameactions.ActionAndConfig(SprintRight, SprintConfig()),
        CrouchToggle(None).name: gameactions.ActionAndConfig(CrouchToggle, CrouchToggleConfig()),
        JournalToggle(None).name: gameactions.ActionAndConfig(JournalToggle, JournalToggleConfig()),
        Place(None).name: gameactions.ActionAndConfig(Place, PlaceConfig()),
        Pickup(None).name: gameactions.ActionAndConfig(Pickup, PickupConfig()),
        Drop(None).name: gameactions.ActionAndConfig(Drop, DropConfig()),
        Switch(None).name: gameactions.ActionAndConfig(Switch, SwitchConfig()),
        TorchToggle(None).name: gameactions.ActionAndConfig(TorchToggle, TorchToggleConfig()),
        Talk(None).name: gameactions.ActionAndConfig(Talk, TalkConfig()),
        Radio(None).name: gameactions.ActionAndConfig(Radio, RadioConfig()),
        LookUp(None).name: gameactions.ActionAndConfig(LookUp, LookUpConfig()),
        LookDown(None).name: gameactions.ActionAndConfig(LookDown, LookDownConfig()),
        LookLeft(None).name: gameactions.ActionAndConfig(LookLeft, LookLeftConfig()),
        LookRight(None).name: gameactions.ActionAndConfig(LookRight, LookRightConfig()),
        PeekUp(None).name: gameactions.ActionAndConfig(PeekUp, PeekUpConfig()),
        PeekDown(None).name: gameactions.ActionAndConfig(PeekDown, PeekDownConfig()),
        PeekLeft(None).name: gameactions.ActionAndConfig(PeekLeft, PeekLeftConfig()),
        PeekRight(None).name: gameactions.ActionAndConfig(PeekRight, PeekRightConfig()),
        Use(None).name: gameactions.ActionAndConfig(Use, UseConfig()),
        Box(None).name: gameactions.ActionAndConfig(Box, BoxConfig()),
        Teabag(None).name: gameactions.ActionAndConfig(Teabag, TeabagConfig()),
        Disco(None).name: gameactions.ActionAndConfig(Disco, DiscoConfig()),
        CycleItems(None).name: gameactions.ActionAndConfig(CycleItems, CycleItemsConfig()),
        CycleItemsAndUse(None).name: gameactions.ActionAndConfig(CycleItemsAndUse, CycleItemsAndUseConfig()),
        DropAllItems(None).name: gameactions.ActionAndConfig(DropAllItems, DropAllItemsConfig()),
        Spin(None).name: gameactions.ActionAndConfig(Spin, SpinConfig()),
        Headbang(None).name: gameactions.ActionAndConfig(Headbang, HeadbangConfig()),
        Yoga(None).name: gameactions.ActionAndConfig(Yoga, YogaConfig()),
        Feet(None).name: gameactions.ActionAndConfig(Feet, FeetConfig()),
        Freeze(None).name: gameactions.ActionAndConfig(Freeze, FreezeConfig()),
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
        Radio(config_fn),
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
        Yoga(config_fn),
        Feet(config_fn),
        Freeze(config_fn),
    ]


def all_actions_dict(config_fn: gameactions.ConfigFn) -> gameactions.ActionDict:
    """Get all actions as a dict"""
    return {action.name: action for action in all_actions(config_fn)}


def default_config() -> gameactions.Config:
    """Get the default config"""
    return gameactions.Config({
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
        Radio(None).name: RadioConfig(),
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
        Yoga(None).name: YogaConfig(),
        Feet(None).name: FeetConfig(),
        Freeze(None).name: FreezeConfig(),
    })
