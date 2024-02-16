#!./.venv/bin/python3
import dataclasses
from typing import ClassVar

from .. import environment, gameactions

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
