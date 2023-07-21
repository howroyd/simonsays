#!./.venv/bin/python3
import concurrent.futures as cf
import functools
import queue

import config as configsaver
import gui
import phasmoactions as pa
import twitchactions as ta
import twitchirc

VERSION = "2.0.0"
CHANNEL = "drgreengiant"


def done_callback(future, command):
    '''Callback for when a command is done'''
    print(f"Done: {command.tag=}")


def make_runtime() -> configsaver.Runtime:
    '''Make the runtime data'''
    keybinds = pa.make_default_keybinds()
    keybinds["walk_forward"] = "up"
    keybinds["crouch"] = "ctrl"
    config = pa.Config(keybinds=keybinds)

    phasmoActions = pa.make_action_list(config)
    phasmoRuntime = ta.make_runtime_dict(phasmoActions, keybinds)
    phasmoRuntime['headbang'].enabled = False

    return configsaver.Runtime(
        version=VERSION,
        channel=CHANNEL,
        action_list=phasmoActions,
        runtime_dict=phasmoRuntime,
        config=config
    )


if __name__ == "__main__":
    runtime = make_runtime()

    print()

    with (cf.ThreadPoolExecutor(max_workers=1) as executor,
            twitchirc.TwitchIrc(CHANNEL) as irc):
        print(f"TwitchIrc initialized to channel {CHANNEL}")

        mygui = gui.make_gui(runtime)

        configsaver.save_config(runtime)

        while True:
            msg: twitchirc.TwitchMessage | None = None
            try:
                queue_msg = irc.queue.get(timeout=0.1)
                msg = twitchirc.TwitchMessage.from_irc_message(queue_msg) if queue_msg else None
            except queue.Empty:
                pass
            mygui.update()

            if not msg:
                continue

            command = msg.payload.lower()

            action = ta.find_command(runtime.action_list, command)

            if action is not None:
                print(f"{command=}: {action.__class__=}")

                runtime_data = runtime.runtime_dict.get(action.tag, None)

                if not runtime_data.can_use:
                    print(f"{action.tag=} can\'t run yet")
                    continue

                runtime_data.use_now()

                future = executor.submit(action.run)
                future.add_done_callback(functools.partial(done_callback, command=action))
