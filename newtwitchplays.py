#!./.venv/bin/python3
import concurrent.futures as cf
import dataclasses
import functools
import queue

# import config as configsaver
# import gui
import phasmoactions
import twitchactions
import twitchirc

VERSION = "2.0.0"
CHANNEL = "drgreengiant"


def done_callback(future, tag):
    """Callback for when a command is done"""
    print(f"Done: {tag=} {future.result()=}")


@dataclasses.dataclass(slots=True)
class GlobalConfig:
    """Global configuration"""
    phasmoconfig: phasmoactions.Config
    twitchconfig: twitchactions.Config


def make_phasmo_actions(globalconfig: GlobalConfig) -> phasmoactions.ActionDict:
    """Make the phasmo actions"""
    def get_phasmo_config() -> phasmoactions.Config:
        """Get the phasmo config"""
        return globalconfig.phasmoconfig
    return phasmoactions.all_actions_dict(get_phasmo_config)


def make_twitch_actions(globalconfig: GlobalConfig) -> twitchactions.ActionDict:
    """Make the twitch actions"""
    def get_twitch_config() -> twitchactions.Config:
        """Get the twitch config"""
        return globalconfig.twitchconfig
    return {key: twitchactions.TwitchAction(get_twitch_config, key, value) for key, value in make_phasmo_actions(globalconfig).items()}


def find_tag_by_command_in_config(twitch_config: twitchactions.Config, command: str) -> str | None:
    """Find a tag by command"""
    return twitch_config.find_by_command(command)


def find_tag_by_command_in_actions(twitch_actions: twitchactions.ActionDict, command: str) -> str | None:
    """Find a tag by command"""
    for key, action in twitch_actions.items():
        if action.check_command(command):
            return key
    return None


if __name__ == "__main__":
    config = GlobalConfig(phasmoconfig=phasmoactions.Config(), twitchconfig=twitchactions.Config())
    myactions = make_twitch_actions(config)

    for key, value in myactions.items():
        config.twitchconfig.config[key] = twitchactions.TwitchActionConfig(key, cooldown=0.5)

    import hidactions

    @dataclasses.dataclass(slots=True)
    class LookActionConfig:
        hidconfig: hidactions.Config

    look_up_hidconfig = hidactions.MouseMoveDirectionActionConfig(500, hidactions.MouseMoveDirection.UP)
    look_up_config = LookActionConfig(hidconfig=look_up_hidconfig)

    config.phasmoconfig.config['look_up'] = look_up_config
    config.twitchconfig.config['headbang'].cooldown = 10

    print()

    with (cf.ThreadPoolExecutor(max_workers=1) as executor,
            twitchirc.TwitchIrc(CHANNEL) as irc):
        print(f"TwitchIrc initialized to channel {CHANNEL}")

        # mygui = gui.make_gui(runtime)

        # configsaver.save_config(runtime)

        while True:
            msg: twitchirc.TwitchMessage | None = None
            try:
                queue_msg = irc.queue.get(timeout=0.1)
                msg = twitchirc.TwitchMessage.from_irc_message(queue_msg) if queue_msg else None
            except queue.Empty:
                pass
            # mygui.update()

            if not msg:
                continue

            command = msg.payload

            tag = find_tag_by_command_in_actions(myactions, command)

            if tag is not None:
                print(f"{command=}: {tag=}")

                # ret = myactions[tag].run()
                # done_callback(ret, tag)

                future = executor.submit(myactions[tag].run)
                future.add_done_callback(functools.partial(done_callback, tag=tag))
