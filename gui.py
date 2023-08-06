#!./.venv/bin/python3
import dataclasses
import functools
import pprint as pp
import tkinter as tk
from typing import Any, Callable

import config as configsaver

KEY_IGNORED_STR = 'ignored'


class Callbacks:
    @staticmethod
    def print_runtime_cb(runtime: configsaver.Runtime, selection: tk.StringVar):
        """Print the runtime data for the selected action"""
        print(selection.get(), end=": ")
        pp.pprint(configsaver.merge_interesting_data(runtime)[selection.get()])

    @staticmethod
    def set_var_cb(runtime: configsaver.Runtime, setter: Callable, selection: tk.StringVar, statevar, *args) -> None:
        """Set the enabled state for the selected action"""
        tag = selection.get()
        state = statevar.get()
        print(f"Set: {state=} for {tag}")
        setter(state)

        configsaver.save_config(runtime)

    @staticmethod
    def set_checkbox_cb(runtime: configsaver.Runtime, setter: Callable[[bool], None], selection: tk.StringVar, statevar: tk.BooleanVar) -> None:
        """Set the enabled state for the selected action"""
        tag = selection.get()
        state = statevar.get()
        print(f"Set enabled: {state=} for {tag}")
        setter(state)

        configsaver.save_config(runtime)

    @staticmethod
    def set_key_cb(runtime: configsaver.Runtime, setter: Callable[[str], None], selection: tk.StringVar, key: tk.StringVar, *args) -> None:
        """Set the enabled state for the selected action"""
        tag = selection.get()
        keybind = key.get()
        print(f"Set keybind: {keybind=} for {tag}")
        setter(keybind)

        configsaver.save_config(runtime)

    @staticmethod
    def set_cooldown_cb(runtime: configsaver.Runtime, selection: tk.StringVar, cooldown: tk.DoubleVar, value: str):
        """Set the cooldown for the selected action"""
        tag = selection.get()
        val = float(value)
        print(f"Set cooldown: {val=} for {tag}")
        runtime.runtime_dict[tag].cooldown = val

        configsaver.save_config(runtime)

    @staticmethod
    def set_random_chance_cb(runtime: configsaver.Runtime, selection: tk.StringVar, random_chance: tk.IntVar, value: str):
        """Set the random chance for the selected action"""
        tag = selection.get()
        val = int(value)
        print(f"Set random_chance: {val=} for {tag}")
        runtime.runtime_dict[tag].random_chance = val

        configsaver.save_config(runtime)


def get_key(runtime: configsaver.Runtime, tag: str) -> str:
    """Get the key (or button) for the action"""
    action = dataclasses.asdict(next((x for x in runtime.action_list if x.tag == tag), None))

    if action['chained']:
        return KEY_IGNORED_STR

    return action.get('key', None) or action.get('button', None) or KEY_IGNORED_STR


def get_command_text(runtime: configsaver.Runtime, tag: str) -> str:
    """Get the command text for the action"""
    action = next((x for x in runtime.action_list if x.tag == tag), None)
    command_text = action.command
    if isinstance(command_text, list):
        command_text = ", ".join(command_text)
    return command_text


def set_command_text(runtime: configsaver.Runtime, tag: str, command_text: str) -> None:
    action = next((x for x in runtime.action_list if x.tag == tag), None)
    action.command = command_text


def set_enabled_state(tk_obj, tk_var, predicate: Callable[[Any], bool]) -> None:
    """Set the state of a Tk object based on a Tk variable and predicate"""
    tk_obj.configure(state=tk.NORMAL if predicate(tk_var.get()) else tk.DISABLED)


def populate_frame(runtime: configsaver.Runtime,
                   selection: tk.StringVar,
                   enabled: tk.BooleanVar,
                   key: tk.StringVar,
                   cooldown: tk.DoubleVar,
                   random_chance: tk.IntVar,
                   command: tk.StringVar,
                   key_entry: tk.Entry) -> None:
    """Populate the frame with the selected action"""
    enabled.set(runtime.runtime_dict[selection.get()].enabled)

    key_in_ram = get_key(runtime, selection.get())
    key.set(key_in_ram)

    set_enabled_state(key_entry, key, lambda x: x != KEY_IGNORED_STR)

    cooldown.set(runtime.runtime_dict[selection.get()].cooldown)
    random_chance.set(runtime.runtime_dict[selection.get()].random_chance)
    command.set(get_command_text(runtime, selection.get()))


def make_window(runtime: configsaver.Runtime, width_px: int, height_px: int) -> tk.Tk:
    """Make the window"""
    window = tk.Tk()
    window.title(f"Twitch Plays v{runtime.version} by DrGreenGiant")
    window.geometry(f"{width_px}x{height_px}")
    return window


def make_canvas(runtime: configsaver.Runtime, image_path: str, *, window: tk.Tk | None = None) -> tk.Canvas:
    """Make the canvas with a background image"""
    # img = tk.PhotoImage(file=image_path)
    from PIL import Image
    width, height = Image.open(image_path).size

    window = window or make_window(runtime, width, height)
    img = tk.PhotoImage(file=image_path)

    canvas = tk.Canvas(window, width=img.width(), height=img.height())
    canvas.pack(expand=True, fill=tk.BOTH)

    canvas.create_image((0, 0), image=img, anchor=tk.N + tk.W)
    canvas.image = img  # Keep a reference to the image to prevent garbage collection
    canvas.create_text((5, 5), text=f"Connected to:\n#{runtime.channel}", anchor=tk.N + tk.W)
    canvas.create_text((img.width() - 5, 5), text=f"Version: {runtime.version}", anchor=tk.N + tk.E)

    window.update()

    return canvas


def make_selection_frame(where, runtime: configsaver.Runtime) -> tuple[tk.Frame, tk.StringVar]:
    """Make the selection frame"""
    frame = tk.Frame(where, width=320, height=50, relief='raised', borderwidth=5)

    selection = tk.StringVar(where)
    selection.set(runtime.action_list[0].tag)

    tk.Label(frame, text="Select action:").pack(side=tk.LEFT, anchor=tk.W, padx=10)
    tk.OptionMenu(frame, selection, *[item.tag for item in runtime.action_list]).pack(side=tk.RIGHT, anchor=tk.E, padx=10)

    return frame, selection


def pack_lhs(thing: tk.Frame) -> None:
    """Pack to the left"""
    thing.pack(side=tk.LEFT, anchor=tk.W)
    # thing.pack_propagate(0)


def pack_rhs(thing: tk.Frame) -> None:
    """Pack to the right"""
    thing.pack(side=tk.RIGHT, anchor=tk.E)
    # thing.pack_propagate(0)


@dataclasses.dataclass(frozen=True, slots=True)
class RuntimeFrames:
    root: tk.Tk
    runtime: configsaver.Runtime
    selection: tk.StringVar
    frame_width: int

    def make_labelled_checkbox_frame(self, name: str, initial_value: bool, setter: Callable[[bool], None]) -> tuple[tk.Frame, tk.BooleanVar]:
        """Make a labelled checkbox frame"""
        frame = tk.Frame(self.root, width=self.frame_width, height=50)

        enabled = tk.BooleanVar(frame)
        enabled.set(initial_value)

        label = tk.Label(frame, text=name, width=25, anchor=tk.E)

        cb = functools.partial(Callbacks.set_var_cb,
                               self.runtime,
                               setter,
                               self.selection,
                               enabled)
        button = tk.Checkbutton(frame, width=25, onvalue=True, offvalue=False, variable=enabled, command=cb, anchor=tk.W)

        pack_lhs(label)
        pack_rhs(button)

        return frame, enabled

    def make_labelled_text_frame(self, name: str, initial_value: str, setter: Callable[[str], None]) -> tuple[tk.Frame, tk.StringVar]:
        """Make the command frame"""
        frame = tk.Frame(self.root, width=self.frame_width, height=50)

        command = tk.StringVar(frame)
        command.set(initial_value)

        cb = functools.partial(Callbacks.set_key_cb,
                               self.runtime,
                               setter,
                               self.selection,
                               command)
        command.trace_add("write", cb)

        label = tk.Label(frame, text=name, width=25, anchor=tk.E)

        entry = tk.Entry(frame, width=33, textvariable=command)

        pack_lhs(label)
        pack_rhs(entry)

        return frame, command


def make_cooldown_frame(where, runtime: configsaver.Runtime, selection: tk.StringVar, frame_width: int) -> tuple[tk.Frame, tk.IntVar]:
    """Make the cooldown frame"""
    frame = tk.Frame(where, width=frame_width, height=50)

    cooldown = tk.IntVar(frame)
    cooldown.set(runtime.runtime_dict[selection.get()].cooldown)

    cb = functools.partial(Callbacks.set_cooldown_cb, runtime, selection, cooldown)

    label = tk.Label(frame, text="Cooldown", width=25, anchor=tk.E)
    # scale = tk.Label(frame, text="Cooldown", width=25, anchor=tk.W)
    scale = tk.Scale(frame, length=200, from_=0, to=60, resolution=1, orient=tk.HORIZONTAL, variable=cooldown, command=cb)

    pack_lhs(label)
    pack_rhs(scale)

    return frame, cooldown


def make_random_frame(where, runtime: configsaver.Runtime, selection: tk.StringVar, frame_width: int) -> tuple[tk.Frame, tk.IntVar]:
    """Make the random frame"""
    frame = tk.Frame(where, width=frame_width, height=50)

    random_chance = tk.IntVar(frame)
    random_chance.set(runtime.runtime_dict[selection.get()].random_chance)

    cb = functools.partial(Callbacks.set_random_chance_cb, runtime, selection, random_chance)

    label = tk.Label(frame, text="Random chance", width=25, anchor=tk.E)
    scale = tk.Scale(frame, length=200, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, variable=random_chance, command=cb)

    pack_lhs(label)
    pack_rhs(scale)

    return frame, random_chance


def make_option_frame(where, runtime: configsaver.Runtime, selection: tk.StringVar) -> tuple[tk.Frame, dict]:
    """Make the option frame"""
    FRAME_WIDTH = 400

    frame = tk.Frame(where, width=FRAME_WIDTH, height=200)
    runtimeframes = RuntimeFrames(frame, runtime, selection, FRAME_WIDTH)

    vars = {}
    name = "Enabled"
    enabled_frame, var = runtimeframes.make_labelled_checkbox_frame(name,
                                                                    runtime.runtime_dict[selection.get()].enabled,
                                                                    lambda state, runtime=runtime, selection=selection:
                                                                    runtime.runtime_dict[selection.get()].set_enabled(state))
    enabled_frame.pack()
    vars[name.lower()] = var

    name = "Command"
    command_frame, var = runtimeframes.make_labelled_text_frame(name,
                                                                get_command_text(runtime, selection.get()),
                                                                lambda state, runtime=runtime, selection=selection:
                                                                set_command_text(runtime, selection.get(), state))
    command_frame.pack()
    vars[name.lower()] = var

    name = "Keybind"
    keybind_frame, var = runtimeframes.make_labelled_text_frame(name,
                                                                get_command_text(runtime, selection.get()),
                                                                lambda state, runtime=runtime, selection=selection:
                                                                set_command_text(runtime, selection.get(), state))
    keybind_frame.pack()
    vars[name.lower()] = var

    cooldown_frame, cooldown = make_cooldown_frame(frame, runtime, selection, FRAME_WIDTH)
    cooldown_frame.pack()
    vars['cooldown'] = cooldown

    random_chance_frame, random_chance = make_random_frame(frame, runtime, selection, FRAME_WIDTH)
    random_chance_frame.pack()
    vars['random_chance'] = random_chance

    return frame, vars


def make_gui(runtime: configsaver.Runtime) -> tk.Tk:
    """Make the GUI"""
    canvas = make_canvas(runtime, "assets/Green_tato_640.png")
    window = canvas.winfo_toplevel()

    vars = {}

    selection_frame, selection = make_selection_frame(canvas, runtime)
    selection_frame.pack(side=tk.TOP, anchor=tk.N, pady=10, expand=True)
    # selection_frame.pack_propagate(0)

    # frame = tk.Frame(canvas, width=400, height=50, relief='raised', borderwidth=5)
    # frame.pack(side=tk.TOP, anchor=tk.N)
    # frame.pack_propagate(0)
    option_frame, newvars = make_option_frame(canvas, runtime, selection)
    option_frame.pack(side=tk.TOP, anchor=tk.N, pady=10, expand=True)
    option_frame.pack_propagate(0)
    vars = vars | newvars

    window.update()
    return window

    column = 0
    row = 0

    selection = tk.StringVar(window)
    selection.set(runtime.action_list[0].tag)

    action_frame = tk.Frame(window, borderwidth=1, relief=tk.RAISED)
    action_frame.grid(column=1, row=row, rowspan=3)
    row += 1

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
