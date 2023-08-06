#!./.venv/bin/python3
import dataclasses
import random
import time

import actions


@dataclasses.dataclass(slots=True)
class TwitchAction(actions.Action):
    action: actions.Action
    command: str | list[str]
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
