#!./.venv/bin/python3
import dataclasses
import random
import time

import actions
import phasmoactions

DEBUG = True


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
            if DEBUG:
                print(f"Action {self.command} is disabled")
            return
        if self.on_cooldown:
            if DEBUG:
                print(f"Action {self.command} is on cooldown")
            return
        if self.random_chance is not None and random.randint(0, 100) > self.random_chance:
            if DEBUG:
                print(f"Action {self.command} failed random chance")
            self.reset_cooldown()
            return
        self._run()

    def _run(self) -> None:
        """Run the action"""
        self.reset_cooldown()
        if DEBUG:
            print(f"Running action {self.command}")
        self.action.run()

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


if __name__ == "__main__":
    import hidactions

    @dataclasses.dataclass(slots=True)
    class LookActionConfig:
        hidconfig: hidactions.Config

    look_up_hidconfig = hidactions.MouseMoveDirectionActionConfig(500, hidactions.MouseMoveDirection.UP)
    look_up_config = LookActionConfig(hidconfig=look_up_hidconfig)
    look_down_hidconfig = hidactions.MouseMoveDirectionActionConfig(250, hidactions.MouseMoveDirection.DOWN)
    look_down_config = LookActionConfig(hidconfig=look_down_hidconfig)

    config = phasmoactions.Config(config={
        "look_up": look_up_config,
        "look_down": look_down_config,
    })

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
    headbang = phasmoactions.Headbang(lambda: config)

    ##

    myactions = phasmoactions.all_actions_dict(lambda: config)

    look_up = TwitchAction(myactions["look_up"], "look up", cooldown=0.5)
    look_down = TwitchAction(myactions["look_down"], "look down", cooldown=0.5)
    headbang = TwitchAction(myactions["headbang"], "headbang", cooldown=0.5)

    myactions = {key: TwitchAction(value, key, cooldown=0.5) for key, value in myactions.items()}

    myactions["look_up"].run()
    myactions["look_down"].run()
    myactions["look_down"].run()
    myactions["headbang"].run()
    myactions["look_down"].run()
