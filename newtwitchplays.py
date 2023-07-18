#!./.venv/bin/python3
import concurrent.futures as cf
import functools
import queue
import tkinter as tk

import phasmoactions as pa
import twitchactions as ta
import twitchirc

VERSION = "2.0.0"
CHANNEL = "drgreengiant"


def done_callback(future, command):
    print(f"Done: {command.tag=}")


def test_callback(tag: str):
    print(f"Test callback: {tag=}")


def set_enabled_cb(runtime_data: tuple[str, ta.RuntimeData], enabled: tk.BooleanVar):
    tag, runtime_data = runtime_data
    state = enabled.get()
    print(f"Set enabled: {state=} for {tag}")
    runtime_data.enabled = state


def make_gui(channel: str, action_list: ta.TwitchActionList, runtime_dict: ta.TwitchRuntimeDict) -> tk.Tk:
    N_COLUMNS = 4

    window = tk.Tk()
    window.title(f"Twitch Plays v{VERSION} by DrGreenGiant")

    tk.Label(window, text=F"Connected to #{CHANNEL}", padx=5, pady=5).grid(column=0, row=0, columnspan=N_COLUMNS, padx=5, pady=5)

    column = 0
    row = 1

    for action in action_list:
        runtime_data = runtime_dict.get(action.tag, None)
        if runtime_data is None:
            continue

        action_frame = tk.Frame(window, borderwidth=1, relief=tk.RAISED)
        action_frame.grid(column=column, row=row, padx=5, pady=5)

        tk.Label(action_frame, text=action.tag, padx=5, pady=5).pack()

        enabled = tk.BooleanVar()
        enabled.set(runtime_data.enabled)
        tk.Checkbutton(action_frame, text="Enabled", padx=5, pady=5, onvalue=True, offvalue=False, variable=enabled, command=functools.partial(set_enabled_cb, (action.tag, runtime_data), enabled)).pack()

        tk.Button(action_frame, text="Test action", padx=5, pady=5, command=functools.partial(test_callback, action.tag)).pack()

        # action_frame.pack()

        column += 1
        if column > (N_COLUMNS - 1):
            column = 0
            row += 1

    window.update()
    return window


if __name__ == "__main__":
    keybinds = pa.make_default_keybinds()
    keybinds["walk_forward"] = "up"
    keybinds["crouch"] = "ctrl"
    config = pa.Config(keybinds=keybinds)

    phasmoActions = pa.make_action_list(config)
    phasmoRuntime = ta.make_runtime_dict(phasmoActions)
    phasmoRuntime['headbang'].enabled = False

    print()

    with (cf.ThreadPoolExecutor(max_workers=1) as executor,
            twitchirc.TwitchIrc(CHANNEL) as irc):
        print(f"TwitchIrc initialized to channel {CHANNEL}")

        gui = make_gui(CHANNEL, phasmoActions, phasmoRuntime)

        while True:
            msg: twitchirc.TwitchMessage | None = None
            try:
                queue_msg = irc.queue.get(timeout=0.1)
                msg = twitchirc.TwitchMessage.from_irc_message(queue_msg) if queue_msg else None
            except queue.Empty:
                pass
            gui.update()

            if not msg:
                continue

            command = msg.payload.lower()

            action = ta.find_command(phasmoActions, command)

            if action is not None:
                print(f"{command=}: {action.__class__=}")

                runtime_data = phasmoRuntime.get(action.tag, None)

                if not runtime_data.can_use:
                    print(f"{action.tag=} can\'t run yet")
                    continue

                runtime_data.use_now()

                future = executor.submit(action.run)
                future.add_done_callback(functools.partial(done_callback, command=action))
