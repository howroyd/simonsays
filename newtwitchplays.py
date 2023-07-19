#!./.venv/bin/python3
import concurrent.futures as cf
import functools
import pprint as pp
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

def print_runtime_cb(runtime_dict: ta.TwitchRuntimeDict, selection: tk.StringVar):
    pprint.pprint(runtime_dict[selection.get()])

def set_enabled_cb(runtime_dict: ta.TwitchRuntimeDict, selection: tk.StringVar, enabled: tk.BooleanVar):
    tag = selection.get()
    state = enabled.get()
    print(f"Set enabled: {state=} for {tag}")
    runtime_dict[tag].enabled = state

def set_cooldown_cb(runtime_dict: ta.TwitchRuntimeDict, selection: tk.StringVar, cooldown: tk.DoubleVar, value: str):
    tag = selection.get()
    val = float(value)
    print(f"Set cooldown: {val=} for {tag}")
    runtime_dict[tag].cooldown = val

def set_random_chance_cb(runtime_dict: ta.TwitchRuntimeDict, selection: tk.StringVar, random_chance: tk.IntVar, value: str):
    tag = selection.get()
    val = int(value)
    print(f"Set random_chance: {val=} for {tag}")
    runtime_dict[tag].random_chance = val

def populate_frame(runtime_dict: ta.TwitchRuntimeDict, selection: tk.StringVar, enabled: tk.BooleanVar, cooldown: tk.DoubleVar, random_chance: tk.IntVar, var, index, mode):
    enabled.set(runtime_dict[selection.get()].enabled)
    cooldown.set(runtime_dict[selection.get()].cooldown)
    random_chance.set(runtime_dict[selection.get()].random_chance)

def make_gui(channel: str, action_list: ta.TwitchActionList, runtime_dict: ta.TwitchRuntimeDict) -> tk.Tk:
    N_COLUMNS = 4

    window = tk.Tk()
    window.title(f"Twitch Plays v{VERSION} by DrGreenGiant")

    column = 0
    row = 0

    tk.Label(window, text=F"Connected to #{CHANNEL}", padx=5, pady=5).grid(column=column, row=row, columnspan=N_COLUMNS, padx=5, pady=5)
    row += 1

    selection = tk.StringVar(window)
    selection.set(action_list[0].tag)

    action_frame = tk.Frame(window, borderwidth=1, relief=tk.RAISED)
    action_frame.grid(column=column, row=row, columnspan=N_COLUMNS, padx=5, pady=5)
    row += 1

    enabled = tk.BooleanVar(action_frame)
    enabled.set(runtime_dict[selection.get()].enabled)
    cb = functools.partial(set_enabled_cb, runtime_dict, selection, enabled)
    tk.Label(action_frame, text="Enabled", padx=5, pady=5).pack()
    tk.Checkbutton(action_frame, text="Enabled", padx=5, pady=5, onvalue=True, offvalue=False, variable=enabled, command=cb).pack()

    cooldown = tk.DoubleVar(action_frame)
    cooldown.set(runtime_dict[selection.get()].cooldown)
    cb = functools.partial(set_cooldown_cb, runtime_dict, selection, cooldown)
    tk.Label(action_frame, text="Cooldown", padx=5, pady=5).pack()
    tk.Scale(action_frame, from_=0.0, to=60.0, resolution=0.1, orient=tk.HORIZONTAL, variable=cooldown, command=cb).pack()

    random_chance = tk.IntVar(action_frame)
    random_chance.set(runtime_dict[selection.get()].random_chance)
    cb = functools.partial(set_random_chance_cb, runtime_dict, selection, random_chance)
    tk.Label(action_frame, text="Random chance", padx=5, pady=5).pack()
    tk.Scale(action_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=random_chance, command=cb).pack()

    cb = functools.partial(print_runtime_cb, runtime_dict, selection)
    tk.Button(action_frame, text="Print runtime", padx=5, pady=5, command=cb).pack()

    tk.OptionMenu(window, selection, *[item.tag for item in action_list]).grid(column=column, row=row, columnspan=N_COLUMNS, padx=5, pady=5)
    row += 1
    selection.trace_add("write", functools.partial(populate_frame, runtime_dict, selection, enabled, cooldown, random_chance))

    # for action in action_list:
    #     runtime_data = runtime_dict.get(action.tag, None)
    #     if runtime_data is None:
    #         continue

    #     action_frame = tk.Frame(window, borderwidth=1, relief=tk.RAISED)
    #     action_frame.grid(column=column, row=row, padx=5, pady=5)

    #     tk.Label(action_frame, text=action.tag, padx=5, pady=5).pack()

    #     enabled = tk.BooleanVar()
    #     enabled.set(runtime_data.enabled)
    #     tk.Checkbutton(action_frame, text="Enabled", padx=5, pady=5, onvalue=True, offvalue=False, variable=enabled, command=functools.partial(set_enabled_cb, (action.tag, runtime_data), enabled)).pack()

    #     tk.Button(action_frame, text="Test action", padx=5, pady=5, command=functools.partial(test_callback, action.tag)).pack()

    #     # action_frame.pack()

    #     column += 1
    #     if column > (N_COLUMNS - 1):
    #         column = 0
    #         row += 1

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
