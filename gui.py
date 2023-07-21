#!./.venv/bin/python3
import dataclasses
import functools
import pprint as pp
import tkinter as tk

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


def populate_frame(runtime: configsaver.Runtime,
                   selection: tk.StringVar,
                   enabled: tk.BooleanVar,
                   key: tk.StringVar,
                   cooldown: tk.DoubleVar,
                   random_chance: tk.IntVar,
                   command: tk.StringVar):
    '''Populate the frame with the selected action'''
    enabled.set(runtime.runtime_dict[selection.get()].enabled)
    key.set(get_key(runtime, selection.get()))
    cooldown.set(runtime.runtime_dict[selection.get()].cooldown)
    random_chance.set(runtime.runtime_dict[selection.get()].random_chance)
    command.set(get_command_text(runtime, selection.get()))


def make_gui(runtime: configsaver.Runtime) -> tk.Tk:
    '''Make the GUI'''
    N_COLUMNS = 4

    window = tk.Tk()
    window.title(f"Twitch Plays v{runtime.version} by DrGreenGiant")

    column = 0
    row = 0

    tk.Label(window, text=F"Connected to #{runtime.channel}", padx=5, pady=5).grid(column=column, row=row, columnspan=N_COLUMNS, padx=5, pady=5)
    row += 1

    selection = tk.StringVar(window)
    selection.set(runtime.action_list[0].tag)

    action_frame = tk.Frame(window, borderwidth=1, relief=tk.RAISED)
    action_frame.grid(column=column, row=row, columnspan=N_COLUMNS, padx=5, pady=5)
    row += 1

    enabled = tk.BooleanVar(action_frame)
    enabled.set(runtime.runtime_dict[selection.get()].enabled)
    cb = functools.partial(set_enabled_cb, runtime, selection, enabled)
    tk.Label(action_frame, text="Enabled", padx=5, pady=5).pack()
    tk.Checkbutton(action_frame, text="Enabled", padx=5, pady=5, onvalue=True, offvalue=False, variable=enabled, command=cb).pack()

    key = tk.StringVar(action_frame)
    key.set(get_key(runtime, selection.get()))
    cb = functools.partial(set_key_cb, runtime, selection, key)
    key.trace_add("write", cb)
    tk.Label(action_frame, text="Keybind/Button", padx=5, pady=5).pack()
    # tk.Entry(action_frame, textvariable=key, validate="focusout", validatecommand=cb).pack()
    tk.Entry(action_frame, textvariable=key).pack()

    cooldown = tk.DoubleVar(action_frame)
    cooldown.set(runtime.runtime_dict[selection.get()].cooldown)
    cb = functools.partial(set_cooldown_cb, runtime, selection, cooldown)
    tk.Label(action_frame, text="Cooldown", padx=5, pady=5).pack()
    tk.Scale(action_frame, from_=0.0, to=60.0, resolution=0.1, orient=tk.HORIZONTAL, variable=cooldown, command=cb).pack()

    random_chance = tk.IntVar(action_frame)
    random_chance.set(runtime.runtime_dict[selection.get()].random_chance)
    cb = functools.partial(set_random_chance_cb, runtime, selection, random_chance)
    tk.Label(action_frame, text="Random chance", padx=5, pady=5).pack()
    tk.Scale(action_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=random_chance, command=cb).pack()

    command = tk.StringVar(action_frame)
    command.set(get_command_text(runtime, selection.get()))
    tk.Label(action_frame, text="Chat command", padx=5, pady=5).pack()
    tk.Entry(action_frame, textvariable=command).pack()

    cb = functools.partial(print_runtime_cb, runtime, selection)
    tk.Button(action_frame, text="Print runtime", padx=5, pady=5, command=cb).pack()

    tk.OptionMenu(window, selection, *[item.tag for item in runtime.action_list]).grid(column=column, row=row, columnspan=N_COLUMNS, padx=5, pady=5)
    row += 1
    cb = functools.partial(populate_frame,
                           runtime,
                           selection,
                           enabled,
                           key,
                           cooldown,
                           random_chance,
                           command)
    selection.trace_add("write", lambda var, index, mode: cb())

    window.update()
    return window
