#!./.venv/bin/python3
import dataclasses
import random
import time
from typing import Callable

import actions
import errorcodes
import phasmoactions

DEBUG = True


@dataclasses.dataclass(slots=True)
class TwitchActionConfig:
    """A config for a Twitch action"""
    command: str | list[str]
    enabled: bool = True
    cooldown: int | None = None
    random_chance: int | None = None

    def check_command(self, command: str) -> bool:
        """Check if the command matches"""
        command = command.lower().lstrip().rstrip()

        if isinstance(self.command, str):
            return command.startswith(self.command)

        for command_ in self.command:
            if command.startswith(command_):
                return True

        return False


ConfigDict = dict[str, TwitchActionConfig]


@dataclasses.dataclass(slots=True)
class Config:
    """The global config for all Twitch actions"""
    config: dict[str, TwitchActionConfig] = dataclasses.field(default_factory=dict)

    def get_config(self, name: str) -> TwitchActionConfig | None:
        """Look up an action config"""
        return self.config.get(name, None)

    def find_by_command(self, command: str) -> TwitchActionConfig | None:
        """Find by Twitch command"""
        for key, item in self.config.items():
            if item.check_command(command):
                return key
        return None


ConfigFn = Callable[[], Config]


@dataclasses.dataclass(slots=True)
class GenericTwitchAction:
    """Generic Twitch action base class"""
    config_fn: ConfigFn

    @property
    def config(self) -> TwitchActionConfig | None:
        """Get the config for this action"""
        return self.config_fn().get_config(self.name)  # TODO: think about relying on self.name existing in child class


@dataclasses.dataclass(slots=True)
class TwitchAction(GenericTwitchAction, actions.Action):
    """A Twitch action"""
    name: str
    action: actions.Action
    last_used: float = 0.0

    def run(self) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: TwitchActionConfig = self.config

        if not actionconfig.enabled:
            if DEBUG:
                print(f"Action {self.name} is disabled")
            return errorcodes.ErrorCode.DISABLED
        if self.on_cooldown:
            if DEBUG:
                print(f"Action {self.name} is on cooldown")
            return errorcodes.ErrorCode.ON_COOLDOWN
        if actionconfig.random_chance is not None and random.randint(0, 100) > actionconfig.random_chance:
            if DEBUG:
                print(f"Action {self.name} failed random chance")
            self.reset_cooldown()
            return errorcodes.ErrorCode.RANDOM_CHANCE

        self.reset_cooldown()

        if DEBUG:
            print(f"Running action {self.name}")

        return self.action.run()

    def check_command(self, command: str) -> bool:
        """Check if the command matches"""
        command = command.lower().lstrip().rstrip()
        actionconfig: TwitchActionConfig = self.config

        if isinstance(actionconfig.command, str):
            return command.startswith(actionconfig.command)

        for command_ in actionconfig.command:
            if command.startswith(command_):
                return True

        return False

    @property
    def on_cooldown(self) -> bool:
        """Whether the action is on cooldown"""
        actionconfig: TwitchActionConfig = self.config

        if actionconfig.cooldown is None:
            return False
        return time.time() - self.last_used < actionconfig.cooldown

    def reset_cooldown(self) -> None:
        """Reset the cooldown"""
        self.last_used = time.time()


ActionDict = dict[str, TwitchAction]


if __name__ == "__main__":
    import hidactions

    @dataclasses.dataclass(slots=True)
    class GlobalConfig:
        phasmoconfig: phasmoactions.Config
        twitchconfig: Config

    @dataclasses.dataclass(slots=True)
    class LookActionConfig:
        hidconfig: hidactions.Config

    phasmo_look_up_hidconfig = hidactions.MouseMoveDirectionActionConfig(500, hidactions.MouseMoveDirection.UP)
    phasmo_look_up_config = LookActionConfig(hidconfig=phasmo_look_up_hidconfig)
    phasmo_look_down_hidconfig = hidactions.MouseMoveDirectionActionConfig(250, hidactions.MouseMoveDirection.DOWN)
    phasmo_look_down_config = LookActionConfig(hidconfig=phasmo_look_down_hidconfig)

    @dataclasses.dataclass(slots=True)
    class PhasmoHeadbangActionConfig:
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

    myphasmoconfig = phasmoactions.Config(config={
        "look_up": phasmo_look_up_config,
        "look_down": phasmo_look_down_config,
        "headbang": PhasmoHeadbangActionConfig(),
    })

    ##

    twitch_look_up_config = TwitchActionConfig("look up", cooldown=0.5)
    twitch_look_down_config = TwitchActionConfig("look down", cooldown=0.5)
    twitch_headbang_config = TwitchActionConfig("look up", cooldown=0.5)

    mytwitchconfig = Config(config={
        "look_up": twitch_look_up_config,
        "look_down": twitch_look_down_config,
        "headbang": twitch_headbang_config,
    })

    global_config = GlobalConfig(myphasmoconfig, mytwitchconfig)

    def get_phasmo_config() -> phasmoactions.Config:
        return global_config.phasmoconfig

    def get_twitch_config() -> Config:
        return global_config.twitchconfig

    myactions = {key: TwitchAction(get_twitch_config, key, value) for key, value in phasmoactions.all_actions_dict(get_phasmo_config).items()}
    myactions["look_up"].run()
    myactions["look_down"].run()
    myactions["look_down"].run()
    myactions["headbang"].run()
    myactions["headbang"].run()
    myactions["headbang"].run()
    myactions["look_down"].run()
