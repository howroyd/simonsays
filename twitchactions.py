#!./.venv/bin/python3
import dataclasses

import actions


@dataclasses.dataclass(slots=True)
class TwitchAction(actions.Action):
    command: str | list[str]
    action: actions.Action
    enabled: bool = True
    cooldown: int | None = None
    last_used: float = 0.0
    random_chance: int | None = None

    def run(self) -> None:
        """Run the action"""
        if not self.enabled:
            return
        if self.on_cooldown:
            return
        if self.random_chance is not None and random.randint(0, 100) > self.random_chance:
            super().reset_cooldown()
            return
        self._run()

    def _run(self) -> None:
        """Run the action"""
        self.reset_cooldown()
        super().run()

    def check_command(self, command: str) -> bool:
        """Check if the command matches"""
        command = command.lower().lstrip().rstrip()

        if isinstance(self.command, str):
            return command.startswith(self.command)

        for command_ in self.command:
            if command.startswith(command_):
                return True

        return False

    @property
    def on_cooldown(self) -> bool:
        """Whether the action is on cooldown"""
        if self.cooldown is None:
            return False
        return time.time() - self.last_used < self.cooldown

    def reset_cooldown(self) -> None:
        """Reset the cooldown"""
        self.last_used = time.time()

    def run(self) -> None:
        """Run the action"""
        self.action.run()

    @property
    def enabled(self) -> bool:
        return self.action.enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self.action.enabled = enabled

    @property
    def on_cooldown(self) -> bool:
        return self.action.on_cooldown

    @property
    def cooldown(self) -> int | None:
        return self.action.cooldown

    @cooldown.setter
    def cooldown(self, cooldown: int | None) -> None:
        self.action.cooldown = cooldown

    @property
    def keybind(self) -> str | None:
        return self.action.keybind

    @keybind.setter
    def keybind(self, keybind: str | None) -> None:
        self.action.keybind = keybind

    @property
    def random_chance(self) -> int | None:
        return self.action.random_chance

    @random_chance.setter
    def random_chance(self, random_chance: int | None) -> None:
        self.action.random_chance = random_chance
