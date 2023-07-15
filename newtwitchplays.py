#!./.venv/bin/python3
import dataclasses
import actions
import pprint
import random

def make_default_keybinds_phasmo() -> dict[str, str]:
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

def get_default_keybind_phasmo(action: str) -> str:
    '''Get the default keybind for Phasmophobia'''
    return make_default_keybinds_phasmo().get(action, None)

@dataclasses.dataclass(frozen=True, slots=True)
class PhasmophobiaPresetActions:
    '''Preset actions for Phasmophobia'''
    keybinds: dict[str, str] = dataclasses.field(default_factory=lambda: make_default_keybinds_phasmo())
    toggle_duration: float = 0.1
    look_distance: float = 500
    peek_distace: float = 250

    ## Keyboard Actions
    def WalkForward(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Walk forward'''
        key = key or self.keybinds.get("walk_forward", None)
        return actions.PressReleaseKey(key, duration or 3) if key else None

    def WalkBackward(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Walk backward'''
        key = key or self.keybinds.get("walk_backward", None)
        return actions.PressReleaseKey(key, duration or 3) if key else None
    
    def WalkLeft(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Walk left'''
        key = key or self.keybinds.get("walk_left", None)
        return actions.PressReleaseKey(key, duration or 3) if key else None
    
    def WalkRight(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Walk right'''
        key = key or self.keybinds.get("walk_right", None)
        return actions.PressReleaseKey(key, duration or 3) if key else None
    
    def CrouchToggle(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Toggle crouch'''
        key = key or self.keybinds.get("crouch", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def JournalToggle(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Toggle journal'''
        key = key or self.keybinds.get("journal", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def Place(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Place'''
        key = key or self.keybinds.get("place", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def Pickup(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Pickup'''
        key = key or self.keybinds.get("pickup", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def Drop(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Drop'''
        key = key or self.keybinds.get("drop", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def SwitchItem(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Switch item'''
        key = key or self.keybinds.get("switch", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def TorchToggle(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Toggle torch'''
        key = key or self.keybinds.get("torch", None)
        return actions.PressReleaseKey(key, duration or self.toggle_duration) if key else None
    
    def Talk(self, *, key: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Talk'''
        key = key or self.keybinds.get("talk", None)
        return actions.PressReleaseKey(key, duration or 10.0) if key else None

    ## Mouse Actions
    def LookUp(self, *, distance: float | None = None) -> actions.Action | None:
        '''Look up'''
        return actions.MoveMouseRelative(0, -(distance or self.look_distance))
    
    def LookDown(self, *, distance: float | None = None) -> actions.Action | None:
        '''Look down'''
        return actions.MoveMouseRelative(0, distance or self.look_distance)
    
    def LookLeft(self, *, distance: float | None = None) -> actions.Action | None:
        '''Look left'''
        return actions.MoveMouseRelative(-(distance or self.look_distance), 0)
    
    def LookRight(self, *, distance: float | None = None) -> actions.Action | None:
        '''Look right'''
        return actions.MoveMouseRelative(distance or self.look_distance, 0)
    
    def PeekUp(self, *, distance: float | None = None) -> actions.Action | None:
        '''Peek up'''
        return actions.MoveMouseRelative(0, -(distance or self.peek_distance))
    
    def PeekDown(self, *, distance: float | None = None) -> actions.Action | None:
        '''Peek down'''
        return actions.MoveMouseRelative(0, distance or self.peek_distance)
    
    def PeekLeft(self, *, distance: float | None = None) -> actions.Action | None:
        '''Peek left'''
        return actions.MoveMouseRelative(-(distance or self.peek_distance), 0)
    
    def PeekRight(self, *, distance: float | None = None) -> actions.Action | None:
        '''Peek right'''
        return actions.MoveMouseRelative(distance or self.peek_distance, 0)
    
    def UseItem(self, *, button: str | None = None, duration: float | None = None) -> actions.Action | None:
        '''Use item'''
        button = button or self.keybinds.get("use", None)
        return actions.PressReleaseButton(button, duration or self.toggle_duration) if button else None

    ## Spicy actions
    def Teabag(self, *, key: str | None = None, pause: float | None = None, repeats: int | None = None) -> actions.Action | None:
        '''Teabag'''
        key = key or self.keybinds.get("crouch", None)
        repeats = repeats or random.randint(5, 10)
        pause = pause or 0.4
        return actions.ActionRepeatWithWait(self.CrouchToggle(key=key), repeats, actions.Wait(pause), recalculate_wait=False)

    def Disco(self, *, key: str | None = None, pause: float | None = None, repeats: int | None = None) -> actions.Action | None:
        '''Disco'''
        key = key or self.keybinds.get("torch", None)
        repeats = repeats or random.randint(5, 10)
        pause = pause or 0.4
        return actions.ActionRepeatWithWait(self.TorchToggle(key=key), repeats, actions.Wait(pause), recalculate_wait=False)
    
    def CycleItems(self, *, key: str | None = None, pause: float | None = None, repeats: int | None = None) -> actions.Action | None:
        '''Cycle items'''
        key = key or self.keybinds.get("switch", None)
        repeats = repeats or random.randint(5, 10)
        pause = pause or 0.4
        return actions.ActionRepeatWithWait(self.SwitchItem(key=key), repeats, actions.Wait(pause), recalculate_wait=False)
    
    def CycleItemsAndUse(self, *, key: str | None = None, button: str | None = None, pause: float | None = None, repeats: int | None = None) -> actions.Action | None:
        '''Cycle items and use'''
        key = key or self.keybinds.get("switch", None)
        button = button or self.keybinds.get("use", None)
        repeats = repeats or 3
        pause = pause or 0.4
        action = actions.ActionSequence([self.SwitchItem(key=key), actions.Wait(pause), self.UseItem(button=button)])
        return actions.ActionRepeatWithWait(action, repeats, actions.Wait(pause))

    def DropAllItems(self, *, key_switch: str | None = None, key_drop: str | None = None, pause: float | None = None, repeats: int | None = None) -> actions.Action | None:
        '''Drop all items'''
        key_switch = key_switch or self.keybinds.get("switch", None)
        key_drop = key_drop or self.keybinds.get("drop", None)
        repeats = repeats or 3
        pause = pause or 0.4
        action = actions.ActionSequence([self.SwitchItem(key=key_switch), actions.Wait(pause), self.Drop(key=key_drop)])
        return actions.ActionRepeatWithWait(action, repeats, actions.Wait(pause))

    def Spin(self, *, distance: int | None = None, pause: float | None = None, repeats: int | None = None, direction: str | None  = None) -> actions.Action | None:
        '''Spin'''
        distance = distance or self.look_distance * 0.1 * random.uniform(0.5, 1.5)  #  Resolution
        pause = pause or 0.05
        repeats = repeats or random.randint(50, 100)  # TODO: calibrate this
        direction = direction or random.choice(["left", "right"])
        print(f"Spin: {distance=:.2f}, {repeats=}, {pause=}, {direction=}")
        if direction == "left":
            return actions.ActionRepeatWithWait(self.LookLeft(distance=distance), repeats, actions.Wait(pause))
        else:
            return actions.ActionRepeatWithWait(self.LookRight(distance=distance), repeats, actions.Wait(pause))

    def Headbang(self, *, distance: int | None = None, pause: float | None = None, repeats: int | None = None) -> actions.Action | None:
        '''Headbang'''
        distance = distance or self.look_distance
        pause = pause or 0.4
        repeats = repeats or random.randint(5, 10)
        action = actions.ActionSequence([self.LookUp(distance=distance), actions.Wait(pause), self.LookDown(distance=distance)])
        return actions.ActionRepeatWithWait(action, repeats, actions.Wait(pause))

if __name__ == "__main__":
    print("Hello World!")

    keybinds = make_default_keybinds_phasmo()
    keybinds["crouch"] = "ctrl"

    preset = PhasmophobiaPresetActions(keybinds)
    pprint.pprint(preset)
    print()
    preset.Headbang().run()

