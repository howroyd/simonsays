#!./.venv/bin/python3
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
    })
    toggle_duration: float = 0.1

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
        '''Pickup and item'''
        key = key or self.keybinds.get("grab", "e")
        return actions.PressReleaseKey(key, self.toggle_duration)


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


if __name__ == "__main__":
    main()
