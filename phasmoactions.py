#!./.venv/bin/python3
import dataclasses
import pprint
import random

import actions
import twitchactions


class Defaults:
    '''Default values'''
    look_distance: float = 500
    peek_distance: float = 250
    toggle_duration: float = 0.1
    walk_duration: float = 3
    talk_duration: float = 10


def make_default_keybinds() -> dict[str, str]:
    '''Make the default keybinds for Phasmophobia'''
    return {
        "walk_forward": "w",
        "walk_backward": "s",
        "walk_left": "a",
        "walk_right": "d",
        "sprint": "shift",
        "crouch": "c",
        "journal": "j",
        "place": "f",
        "pickup": "e",
        "drop": "g",
        "switch": "q",
        "torch": "t",
        "talk": "v",
        "use": "rmb",
    }


def get_default_keybind(action: str) -> str:
    '''Get the default keybind for a Phasmophobia action'''
    return make_default_keybinds().get(action, None)


@dataclasses.dataclass(frozen=True, slots=True)
class Config:
    '''Configuration for Phasmophobia'''
    keybinds: dict[str, str] = dataclasses.field(default_factory=lambda: make_default_keybinds())
    look_distance: float = Defaults.look_distance
    peek_distance: float = Defaults.peek_distance
    toggle_duration: float = Defaults.toggle_duration


def _set_key(obj, tag: str | None = None, member: str | None = None):
    '''Set the key for a frozen dataclass object.  This is a bit nasty.'''
    object.__setattr__(obj,
                       member or "key",
                       object.__getattribute__(obj, member or "key") or obj.config.keybinds.get(obj.tag, get_default_keybind(tag or obj.tag)))


@dataclasses.dataclass(frozen=True, slots=True)
class WalkForward:
    '''Walk forward'''
    config: Config
    key: str | None = None
    duration: float = Defaults.walk_duration
    tag: str = "walk_forward"
    command: str | list[str] = "forward"

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key, self.duration).run()


@dataclasses.dataclass(frozen=True, slots=True)
class WalkBackward:
    '''Walk backward'''
    config: Config
    key: str | None = None
    duration: float = Defaults.walk_duration
    tag: str = "walk_backward"
    command: str | list[str] = dataclasses.field(default_factory=lambda: ["back", "backward"])

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key, self.duration).run()


@dataclasses.dataclass(frozen=True, slots=True)
class WalkLeft:
    '''Walk left'''
    config: Config
    key: str | None = None
    duration: float = Defaults.walk_duration
    tag: str = "walk_left"
    command: str | list[str] = "left"

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key, self.duration).run()


@dataclasses.dataclass(frozen=True, slots=True)
class WalkRight:
    '''Walk right'''
    config: Config
    key: str | None = None
    duration: float = Defaults.walk_duration
    tag: str = "walk_right"
    command: str | list[str] = "right"

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key, self.duration).run()


@dataclasses.dataclass(frozen=True, slots=True)
class CrouchToggle:
    '''Toggle crouch'''
    config: Config
    key: str | None = None
    tag: str = "crouch"
    command: str | list[str] = "crouch"

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class JournalToggle:
    '''Toggle journal'''
    config: Config
    key: str | None = None
    tag: str = "journal"
    command: str | list[str] = "journal"

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Place:
    '''Place'''
    config: Config
    key: str | None = None
    tag: str = "place"
    command: str | list[str] = "place"

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Pickup:
    '''Pickup'''
    config: Config
    key: str | None = None
    tag: str = "pickup"
    command: str | list[str] = dataclasses.field(default_factory=lambda: ["pickup", "grab"])

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Drop:
    '''Drop'''
    config: Config
    key: str | None = None
    tag: str = "drop"
    command: str | list[str] = dataclasses.field(default_factory=lambda: ["drop", "throw"])

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class SwitchItem:
    '''Switch item'''
    config: Config
    key: str | None = None
    tag: str = "switch"
    command: str | list[str] = dataclasses.field(default_factory=lambda: ["switch", "swap"])

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class TorchToggle:
    '''Toggle torch'''
    config: Config
    key: str | None = None
    tag: str = "torch"
    command: str | list[str] = dataclasses.field(default_factory=lambda: ["torch", "light", "flashlight"])

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Talk:
    '''Talk'''
    config: Config
    key: str | None = None
    duration: float = Defaults.talk_duration
    tag: str = "talk"
    command: str | list[str] = dataclasses.field(default_factory=lambda: ["talk", "speak"])

    def __post_init__(self) -> None:
        _set_key(self)

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseKey(self.key, self.duration).run()


@dataclasses.dataclass(frozen=True, slots=True)
class LookUp:
    '''Look up'''
    config: Config
    distance: float = Defaults.look_distance
    tag: str = "look_up"
    command: str | list[str] = "look up"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(0, -self.distance).run()


@dataclasses.dataclass(frozen=True, slots=True)
class LookDown:
    '''Look down'''
    config: Config
    distance: float = Defaults.look_distance
    tag: str = "look_down"
    command: str | list[str] = "look down"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(0, self.distance).run()


@dataclasses.dataclass(frozen=True, slots=True)
class LookLeft:
    '''Look left'''
    config: Config
    distance: float = Defaults.look_distance
    tag: str = "look_left"
    command: str | list[str] = "look left"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(-self.distance, 0).run()


@dataclasses.dataclass(frozen=True, slots=True)
class LookRight:
    '''Look right'''
    config: Config
    distance: float = Defaults.look_distance
    tag: str = "look_right"
    command: str | list[str] = "look right"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(self.distance, 0).run()


@dataclasses.dataclass(frozen=True, slots=True)
class PeekUp:
    '''Peek up'''
    config: Config
    distance: float = Defaults.peek_distance
    tag: str = "peek_up"
    command: str | list[str] = "peek up"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(0, -self.distance).run()


@dataclasses.dataclass(frozen=True, slots=True)
class PeekDown:
    '''Peek down'''
    config: Config
    distance: float = Defaults.peek_distance
    tag: str = "peek_down"
    command: str | list[str] = "peek down"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(0, self.distance).run()


@dataclasses.dataclass(frozen=True, slots=True)
class PeekLeft:
    '''Peek left'''
    config: Config
    distance: float = Defaults.peek_distance
    tag: str = "peek_left"
    command: str | list[str] = "peek left"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(-self.distance, 0).run()


@dataclasses.dataclass(frozen=True, slots=True)
class PeekRight:
    '''Peek right'''
    config: Config
    distance: float = Defaults.peek_distance
    tag: str = "peek_right"
    command: str | list[str] = "peek right"

    def run(self) -> None:
        '''Run the action'''
        actions.MoveMouseRelative(self.distance, 0).run()


@dataclasses.dataclass(frozen=True, slots=True)
class UseItem:
    '''Use item'''
    config: Config
    button: str | None = None
    tag: str = "use"
    command: str | list[str] = "use"

    def __post_init__(self) -> None:
        _set_key(self, member="button")

    def run(self) -> None:
        '''Run the action'''
        actions.PressReleaseButton(self.button).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Teabag:
    '''Teabag'''
    config: Config
    key: str | None = None
    pause: float = 0.4
    repeats: int | None = None
    tag: str = "teabag"
    command: str | list[str] = "teabag"

    def __post_init__(self) -> None:
        _set_key(self, "crouch")

    def run(self) -> None:
        '''Run the action'''
        repeats = self.repeats or random.randint(5, 10)
        actions.ActionRepeatWithWait(CrouchToggle(self.config, key=self.key), repeats, actions.Wait(self.pause)).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Disco:
    '''Disco'''
    config: Config
    key: str | None = None
    pause: float = 0.4
    repeats: int | None = None
    tag: str = "disco"
    command: str | list[str] = "disco"

    def __post_init__(self) -> None:
        _set_key(self, "torch")

    def run(self) -> None:
        '''Run the action'''
        repeats = self.repeats or random.randint(5, 10)
        actions.ActionRepeatWithWait(TorchToggle(self.config, key=self.key), repeats, actions.Wait(self.pause)).run()


@dataclasses.dataclass(frozen=True, slots=True)
class CycleItems:
    '''Cycle items'''
    config: Config
    key: str | None = None
    pause: float = 0.4
    repeats: int | None = None
    tag: str = "cycle_items"
    command: str | list[str] = "cycle"

    def __post_init__(self) -> None:
        _set_key(self, "switch")

    def run(self) -> None:
        '''Run the action'''
        repeats = self.repeats or random.randint(5, 10)
        actions.ActionRepeatWithWait(SwitchItem(self.config, key=self.key), repeats, actions.Wait(self.pause)).run()


@dataclasses.dataclass(frozen=True, slots=True)
class CycleItemsAndUse:
    '''Cycle items and use'''
    config: Config
    key_switch: str | None = None
    button_use: str | None = None
    pause: float = 0.4
    repeats: int = 3
    tag: str = "cycle_items_and_use"
    command: str | list[str] = "chaos"

    def __post_init__(self) -> None:
        _set_key(self, "switch", "key_switch")
        _set_key(self, "use", "button_use")

    def run(self) -> None:
        '''Run the action'''
        sequence = actions.ActionSequence([SwitchItem(self.config, key=self.key_switch), actions.Wait(self.pause), UseItem(self.config, button=self.button_use)])
        actions.ActionRepeatWithWait(sequence, self.repeats, actions.Wait(self.pause)).run()


@dataclasses.dataclass(frozen=True, slots=True)
class DropAllItems:
    '''Drop all items'''
    config: Config
    key_switch: str | None = None
    key_drop: str | None = None
    pause: float = 0.4
    repeats: int = 3
    tag: str = "drop_all_items"
    command: str | list[str] = "yeet"

    def __post_init__(self) -> None:
        _set_key(self, "switch", "key_switch")
        _set_key(self, "drop", "key_drop")

    def run(self) -> None:
        '''Run the action'''
        repeats = self.repeats or 3
        action = actions.ActionSequence([SwitchItem(self.config, key=self.key_switch), actions.Wait(self.pause), Drop(self.config, key=self.key_drop)])
        actions.ActionRepeatWithWait(action, repeats, actions.Wait(self.pause)).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Spin:
    '''Spin'''
    config: Config
    distance: float | None = None
    direction: str | None = None
    pause: float = 0.05
    repeats: int | None = None
    distance: float = Defaults.look_distance * 0.1 * random.uniform(0.5, 1.5)
    tag: str = "spin"
    command: str | list[str] = "spin"

    def run(self) -> None:
        '''Run the action'''
        distance = self.distance or self.look_distance * 0.1 * random.uniform(0.5, 1.5)  # Resolution
        direction = self.direction or random.choice(["left", "right"])
        repeats = self.repeats or random.randint(50, 100)  # TODO: calibrate this
        if direction == "left":
            actions.ActionRepeatWithWait(LookLeft(self.config, distance=distance), repeats, actions.Wait(self.pause)).run()
        else:
            actions.ActionRepeatWithWait(LookRight(self.config, distance=distance), repeats, actions.Wait(self.pause)).run()


@dataclasses.dataclass(frozen=True, slots=True)
class Headbang:
    '''Headbang'''
    config: Config
    distance: float = Defaults.look_distance
    pause: float = 0.4
    repeats: int | None = None
    tag: str = "headbang"
    command: str | list[str] = "headbang"

    def run(self) -> None:
        '''Run the action'''
        repeats = self.repeats or random.randint(5, 10)
        action = actions.ActionSequence([LookUp(self.config, distance=self.distance), actions.Wait(self.pause), LookDown(self.config, distance=self.distance)])
        actions.ActionRepeatWithWait(action, repeats, actions.Wait(self.pause)).run()


def make_action_list(config: Config) -> twitchactions.TwitchActionList:
    '''Make a dictionary of tags and actions'''
    return [
        WalkForward(config),
        WalkBackward(config),
        WalkLeft(config),
        WalkRight(config),
        CrouchToggle(config),
        JournalToggle(config),
        Place(config),
        Pickup(config),
        Drop(config),
        SwitchItem(config),
        TorchToggle(config),
        Talk(config),
        UseItem(config),
        LookUp(config),
        LookDown(config),
        LookLeft(config),
        LookRight(config),
        PeekUp(config),
        PeekDown(config),
        PeekLeft(config),
        PeekRight(config),
        Teabag(config),
        Disco(config),
        CycleItems(config),
        CycleItemsAndUse(config),
        DropAllItems(config),
        Spin(config),
        Headbang(config),
    ]


if __name__ == "__main__":
    print("Hello World!")

    config = Config()
    config.keybinds["crouch"] = "ctrl"

    phasmoActions = make_action_list(config)
    pprint.pprint(twitchactions.command_dict(phasmoActions))

    print()

    commands = ["yeet", "throw", "look up", "crouch", "bullshit"]

    for command in commands:
        action = twitchactions.find_command(phasmoActions, command)

        print(f"{command=}: {action.__class__=}\n")

        if action is not None:
            action.run()
