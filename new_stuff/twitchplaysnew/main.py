#!./.venv/bin/python3
import random
import dataclasses
import actions
import pprint


@dataclasses.dataclass(frozen=True, slots=True)
class PhasmophobiaPresetActions:
    '''Preset actions'''
    keybinds: dict[str, str] = dataclasses.field(default_factory=lambda: {
        "walk_forward": "w",
        "walk_backward": "s",
        "walk_left": "a",
        "walk_right": "d",
        "crouch": "c",
        "journal": "j",
        "place": "f",
        "grab": "e",
        "drop": "g",
        "switch": "q",
        "torch": "t",
        "talk": "v",
    })
    toggle_duration: float = 0.1
    look_distance: int = 500
    peek_distance: int = 250

    ## Keyboard actions
    def WalkForward(self, *, key: str | None = None, duration: float | None = None) -> actions.ActionSequence:
        '''Walk forward'''
        key = key or self.keybinds.get("walk_forward", "w")
        return actions.PressReleaseKey(key, duration or 1.0)

    def WalkBackward(self, *, key: str | None = None, duration: float | None = None) -> actions.ActionSequence:
        '''Walk backward'''
        key = key or self.keybinds.get("walk_backward", "s")
        return actions.PressReleaseKey(key, duration or 1.0)

    def WalkLeft(self, *, key: str | None = None, duration: float | None = None) -> actions.ActionSequence:
        '''Walk left'''
        key = key or self.keybinds.get("walk_left", "a")
        return actions.PressReleaseKey(key, duration or 1.0)

    def WalkRight(self, *, key: str | None = None, duration: float | None = None) -> actions.ActionSequence:
        '''Walk right'''
        key = key or self.keybinds.get("walk_right", "d")
        return actions.PressReleaseKey(key, duration or 1.0)

    def CrouchToggle(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Toggle crouch'''
        key = key or self.keybinds.get("crouch", "c")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def JournalToggle(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Toggle journal'''
        key = key or self.keybinds.get("journal", "j")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def Place(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Place an item'''
        key = key or self.keybinds.get("place", "f")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def Grab(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Pickup an item'''
        key = key or self.keybinds.get("grab", "e")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def Drop(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Drop/throw an item'''
        key = key or self.keybinds.get("drop", "g")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def SwitchItem(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Switch to the next item in the inventory'''
        key = key or self.keybinds.get("switch", "q")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def TorchToggle(self, *, key: str | None = None) -> actions.ActionSequence:
        '''Toggle torch on/off'''
        key = key or self.keybinds.get("torch", "t")
        return actions.PressReleaseKey(key, self.toggle_duration)

    def Talk(self, *, key: str | None = None, duration: float | None = None) -> actions.ActionSequence:
        '''Talk on the radio'''
        key = key or self.keybinds.get("talk", "v")
        return actions.PressReleaseKey(key, duration or 10.0)

    ## Mouse actions
    def UseItem(self, *, button: str | None = None) -> actions.ActionSequence:
        '''Use the item in your hand'''
        button = button or "right"
        return actions.PressReleaseButton(button, self.toggle_duration)

    def LookUp(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Look up'''
        distance = distance or self.look_distance
        return actions.MoveMouseRelative(0, -distance)

    def LookDown(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Look down'''
        distance = distance or self.look_distance
        return actions.MoveMouseRelative(0, distance)

    def LookLeft(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Look left'''
        distance = distance or self.look_distance
        return actions.MoveMouseRelative(-distance, 0)

    def LookRight(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Look right'''
        distance = distance or self.look_distance
        return actions.MoveMouseRelative(distance, 0)

    def PeekUp(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Peek up'''
        distance = distance or self.peek_distance
        return actions.MoveMouseRelative(0, -distance)

    def PeekDown(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Peek down'''
        distance = distance or self.peek_distance
        return actions.MoveMouseRelative(0, distance)

    def PeekLeft(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Peek left'''
        distance = distance or self.peek_distance
        return actions.MoveMouseRelative(-distance, 0)

    def PeekRight(self, *, distance: int | None = None) -> actions.ActionSequence:
        '''Peek right'''
        distance = distance or self.peek_distance
        return actions.MoveMouseRelative(distance, 0)

    ## Spicy actions
    def Teabag(self, *, key: str | None = None, duration: float | None = None, repeats: int | None = None) -> actions.ActionSequence:
        '''Teabag.  If `repeats` is `None` it will be a random number between 5 and 10.  `duration` is the time between toggles'''
        key = key or self.keybinds.get("crouch", "c")
        duration = duration or 0.4
        repeats = repeats or random.randint(5, 10)
        return actions.ActionRepeatWithWait(self.CrouchToggle(key=key), repeats, duration)

    def Disco(self, *, key: str | None = None, duration: float | None = None, repeats: int | None = None) -> actions.ActionSequence:
        '''Disco, turn on and off the torch.  If `repeats` is `None` it will be a random number between 5 and 10.  `duration` is the time between toggles'''
        key = key or self.keybinds.get("torch", "t")
        duration = duration or 0.4
        repeats = repeats or random.randint(5, 10)
        print(f"Disco: {key=}, {repeats=}, {duration=}")
        return actions.ActionRepeatWithWait(self.TorchToggle(key=key), repeats, duration)

    def CycleItems(self, *, key: str | None = None, duration: float | None = None, repeats: int | None = None) -> actions.ActionSequence:
        '''Cycle items.  If `repeats` is `None` it will be a random number between 5 and 10.  `duration` is the time between toggles'''
        key = key or self.keybinds.get("switch", "q")
        duration = duration or 0.4
        repeats = repeats or random.randint(5, 10)
        print(f"CycleItems: {key=}, {repeats=}, {duration=}")
        return actions.ActionRepeatWithWait(self.SwitchItem(key=key), repeats, duration)

    def CycleItemsAndUse(self, *, key: str | None = None, button: str | None = None, duration: float | None = None, repeats: int | None = None) -> actions.ActionSequence:
        '''Cycle items and use them.  If `repeats` is `None` it will be a random number between 1 and 3.  `duration` is the time between toggles'''
        key = key or self.keybinds.get("switch", "q")
        button = button or "right"
        duration = duration or 0.4
        repeats = repeats or random.randint(1, 3)
        sequence = actions.ActionSequence([self.SwitchItem(key=key), actions.Wait(duration), self.UseItem(button=button)])
        print(f"CycleItemsAndUse: {key=}, {button=}, {repeats=}, {duration=}")
        return actions.ActionRepeatWithWait(sequence, repeats, duration)

    def Spin(self, *, distance: int | None = None, duration: float | None = None, repeats: int | None = None, direction: str = None) -> actions.ActionSequence:
        '''Spin.  If `repeats` is `None` it will be a random number between 5 and 10.  If `direction` is `None` it will be a random choice between "left" and "right".  If `distance` is `None` it will be a random number between 0.5 and 1.5 times the look distance.  `duration` is the time between toggles'''
        distance = distance or self.look_distance * random.uniform(0.5, 1.5)
        duration = duration or 0.1
        repeats = repeats or random.randint(5, 10)
        direction = direction or random.choice(["left", "right"])
        print(f"Spin: {distance=}, {repeats=}, {duration=}, {direction=}")
        if direction == "left":
            return actions.ActionRepeatWithWait(self.LookLeft(distance=distance), repeats, duration)
        else:  # Anything other than "left"
            return actions.ActionRepeatWithWait(self.LookRight(distance=distance), repeats, duration)

def main() -> None:
    print("Hello World!")
    phasmo_keybinds = PhasmophobiaPresetActions().keybinds
    print("Default keybinds:")
    pprint.pprint(phasmo_keybinds)

    phasmo_keybinds["walk_forward"] = "up"
    print("New keybinds:")
    pprint.pprint(phasmo_keybinds)

    phasmo_actions = PhasmophobiaPresetActions(phasmo_keybinds)
    phasmo_actions.WalkForward().run()

    #phasmo_actions.CycleItemsAndUse().run()
    phasmo_actions.Spin().run()

if __name__ == "__main__":
    main()
