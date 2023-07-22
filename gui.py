#!./.venv/bin/python3
import dataclasses
import functools
import pprint as pp
import tkinter as tk
from typing import Any, Callable

import config as configsaver

KEY_IGNORED_STR = 'ignored'


def print_runtime_cb(runtime: configsaver.Runtime, selection: tk.StringVar):
    '''Print the runtime data for the selected action'''
    print(selection.get(), end=": ")
    pp.pprint(configsaver.merge_interesting_data(runtime)[selection.get()])


def set_enabled_cb(runtime: configsaver.Runtime, selection: tk.StringVar, enabled: tk.BooleanVar):
    '''Set the enabled state for the selected action'''
    tag = selection.get()
    state = enabled.get()
    print(f"Set enabled: {state=} for {tag}")
    runtime.runtime_dict[tag].enabled = state

    configsaver.save_config(runtime)


def set_key_cb(runtime: configsaver.Runtime, selection: tk.StringVar, key: tk.StringVar, name, index, mode):
    '''Set the enabled state for the selected action'''
    tag = selection.get()
    keybind = key.get()
    print(f"Set keybind: {keybind=} for {tag}")
    runtime.runtime_dict[tag].key = keybind

    configsaver.save_config(runtime)


def set_cooldown_cb(runtime: configsaver.Runtime, selection: tk.StringVar, cooldown: tk.DoubleVar, value: str):
    '''Set the cooldown for the selected action'''
    tag = selection.get()
    val = float(value)
    print(f"Set cooldown: {val=} for {tag}")
    runtime.runtime_dict[tag].cooldown = val

    configsaver.save_config(runtime)


def set_random_chance_cb(runtime: configsaver.Runtime, selection: tk.StringVar, random_chance: tk.IntVar, value: str):
    '''Set the random chance for the selected action'''
    tag = selection.get()
    val = int(value)
    print(f"Set random_chance: {val=} for {tag}")
    runtime.runtime_dict[tag].random_chance = val

    configsaver.save_config(runtime)


def get_key(runtime: configsaver.Runtime, tag: str) -> str:
    '''Get the key (or button) for the action'''
    action = dataclasses.asdict(next((x for x in runtime.action_list if x.tag == tag), None))

    if action['chained']:
        return KEY_IGNORED_STR

    return action.get('key', None) or action.get('button', None) or KEY_IGNORED_STR


def get_command_text(runtime: configsaver.Runtime, tag: str) -> str:
    '''Get the command text for the action'''
    action = next((x for x in runtime.action_list if x.tag == tag), None)
    command_text = action.command
    if isinstance(command_text, list):
        command_text = ", ".join(command_text)
    return command_text


def set_enabled_state(tk_obj, tk_var, predicate: Callable[Any, [bool]]) -> None:
    '''Set the state of a Tk object based on a Tk variable and predicate'''
    tk_obj.configure(state=tk.NORMAL if predicate(tk_var.get()) else tk.DISABLED)


def populate_frame(runtime: configsaver.Runtime,
                   selection: tk.StringVar,
                   enabled: tk.BooleanVar,
                   key: tk.StringVar,
                   cooldown: tk.DoubleVar,
                   random_chance: tk.IntVar,
                   command: tk.StringVar,
                   key_entry: tk.Entry) -> None:
    '''Populate the frame with the selected action'''
    enabled.set(runtime.runtime_dict[selection.get()].enabled)

    key_in_ram = get_key(runtime, selection.get())
    key.set(key_in_ram)

    set_enabled_state(key_entry, key, lambda x: x != KEY_IGNORED_STR)

    cooldown.set(runtime.runtime_dict[selection.get()].cooldown)
    random_chance.set(runtime.runtime_dict[selection.get()].random_chance)
    command.set(get_command_text(runtime, selection.get()))


def make_gui(runtime: configsaver.Runtime) -> tk.Tk:
    '''Make the GUI'''
    N_COLUMNS = 3
    WIDTH = 640
    HEIGHT = 640

    window = tk.Tk()
    window.title(f"Twitch Plays v{runtime.version} by DrGreenGiant")
    window.geometry(f"{WIDTH}x{HEIGHT}")
    # window.state("zoomed")  # Maximised
    # window.configure(bg="blue")

    canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
    canvas.grid(column=0, row=0, rowspan=6, columnspan=N_COLUMNS)

    bg = tk.PhotoImage(file="assets/Green_tato_640.png")
    bg_label = canvas.create_image((0, 0), image=bg, anchor=tk.N + tk.W)
    canvas.image = bg
    canvas.create_text((5, 5), text=f"Connected to:\n#{runtime.channel}", anchor=tk.N + tk.W)
    canvas.create_text((WIDTH - 5, 5), text=f"Version: {runtime.version}", anchor=tk.N + tk.E)

    column = 0
    row = 0

    selection = tk.StringVar(window)
    selection.set(runtime.action_list[0].tag)

    action_frame = tk.Frame(window, borderwidth=1, relief=tk.RAISED)
    action_frame.grid(column=1, row=row, rowspan=3)
    row += 1

    enabled_frame = tk.Frame(action_frame, relief=tk.RAISED, borderwidth=10)
    tk.Label(enabled_frame, text="Enabled", width=20, padx=5, pady=5).grid(row=0, column=0)
    enabled = tk.BooleanVar(enabled_frame)
    enabled.set(runtime.runtime_dict[selection.get()].enabled)
    cb = functools.partial(set_enabled_cb, runtime, selection, enabled)
    tk.Checkbutton(enabled_frame, text="Enabled", padx=5, pady=5, width=20, onvalue=True, offvalue=False, variable=enabled, command=cb).grid(row=0, column=1)
    enabled_frame.pack()

    key_frame = tk.Frame(action_frame, relief=tk.RAISED, borderwidth=10)
    key = tk.StringVar(key_frame)
    key_in_ram = get_key(runtime, selection.get())
    key.set(key_in_ram)
    cb = functools.partial(set_key_cb, runtime, selection, key)
    key.trace_add("write", cb)
    tk.Label(key_frame, text="Keybind/Button", width=20, padx=5, pady=5).grid(row=0, column=0)
    key_entry = tk.Entry(key_frame, width=20, textvariable=key)
    set_enabled_state(key_entry, key, lambda x: x != KEY_IGNORED_STR)
    key_entry.grid(row=0, column=1)
    key_frame.pack()

    cooldown_frame = tk.Frame(action_frame, relief=tk.RAISED, borderwidth=10)
    cooldown = tk.DoubleVar(cooldown_frame)
    cooldown.set(runtime.runtime_dict[selection.get()].cooldown)
    cb = functools.partial(set_cooldown_cb, runtime, selection, cooldown)
    tk.Label(cooldown_frame, text="Cooldown", width=20, padx=5, pady=5).grid(row=0, column=0)
    tk.Scale(cooldown_frame, from_=0, to=60, resolution=1, width=20, orient=tk.HORIZONTAL, variable=cooldown, command=cb).grid(row=0, column=1)
    cooldown_frame.pack()

    random_frame = tk.Frame(action_frame, relief=tk.RAISED, borderwidth=10)
    random_chance = tk.IntVar(random_frame)
    random_chance.set(runtime.runtime_dict[selection.get()].random_chance)
    cb = functools.partial(set_random_chance_cb, runtime, selection, random_chance)
    tk.Label(random_frame, text="Random chance", width=20, padx=5, pady=5).grid(row=0, column=0)
    tk.Scale(random_frame, from_=0, to=100, width=20, orient=tk.HORIZONTAL, variable=random_chance, command=cb).grid(row=0, column=1)
    random_frame.pack()

    command_frame = tk.Frame(action_frame, relief=tk.RAISED, borderwidth=10)
    command = tk.StringVar(command_frame)
    command.set(get_command_text(runtime, selection.get()))
    tk.Label(command_frame, text="Chat command", width=20, padx=5, pady=5).grid(row=0, column=0)
    tk.Entry(command_frame, width=20, textvariable=command).grid(row=0, column=1)
    command_frame.pack()

    print_frame = tk.Frame(action_frame)
    cb = functools.partial(print_runtime_cb, runtime, selection)
    tk.Button(print_frame, text="Print runtime", padx=5, pady=5, command=cb).pack()
    print_frame.pack()

    tk.OptionMenu(window, selection, *[item.tag for item in runtime.action_list]).grid(column=2, row=5)
    row += 1
    cb = functools.partial(populate_frame,
                           runtime,
                           selection,
                           enabled,
                           key,
                           cooldown,
                           random_chance,
                           command,
                           key_entry)
    selection.trace_add("write", lambda var, index, mode: cb())

    window.update()
    return window
