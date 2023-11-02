#!./.venv/bin/python3
import dataclasses
import functools
import multiprocessing as mp
import os
import pprint as pp
import tkinter as tk
from collections.abc import Iterable
from typing import Any, Callable, NoReturn, Optional

import semantic_version

from . import config, environment, hidactions

KEY_IGNORED_STR = 'ignored'


def on_closing(exit_event: Optional[mp.Event] = None) -> NoReturn:
    """Exit the program when window is closed"""
    if exit_event is None:
        print("GUI closed, exiting...")
        os._exit(0)
    exit_event.set()


class Callbacks:
    """Callbacks for the GUI"""
    @staticmethod
    def print_runtime_cb(cfg: config.Config, selection: tk.StringVar):
        """Print the runtime data for the selected action"""
        print(selection.get(), end=": ")
        pp.pprint(cfg[selection.get()])

    @staticmethod
    def set_var_cb(cfg: config.Config, setter: Callable, selection: tk.StringVar, statevar, *args) -> None:
        """Set the enabled state for the selected action"""
        tag = selection.get()
        state = statevar.get()
        print(f"Set: {state=} for {tag}")
        setter(state)

        cfg.save()

    @staticmethod
    def set_checkbox_cb(cfg: config.Config, setter: Callable[[bool], None], selection: tk.StringVar, statevar: tk.BooleanVar) -> None:
        """Set the enabled state for the selected action"""
        tag = selection.get()
        state = statevar.get()
        print(f"Set enabled: {state=} for {tag}")
        setter(state)

        cfg.save()

    @staticmethod
    def set_key_cb(cfg: config.Config, setter: Callable[[str], None], selection: tk.StringVar, key: tk.StringVar, *args) -> None:
        """Set the enabled state for the selected action"""
        tag = selection.get()
        keybind = key.get()
        print(f"Set keybind: {keybind=} for {tag}")
        setter(keybind)

        cfg.save()

    @staticmethod
    def set_cooldown_cb(cfg: config.Config, selection: tk.StringVar, cooldown: tk.DoubleVar, value: str):
        """Set the cooldown for the selected action"""
        tag = selection.get()
        val = float(value)
        print(f"Set cooldown: {val=} for {tag}")
        cfg.config[tag].twitch.cooldown = val

        cfg.save()

    @staticmethod
    def set_random_chance_cb(cfg: config.Config, selection: tk.StringVar, random_chance: tk.IntVar, value: str):
        """Set the random chance for the selected action"""
        tag = selection.get()
        val = int(value)
        print(f"Set random_chance: {val=} for {tag}")
        cfg.config[tag].twitch.random_chance = val

        cfg.save()


def get_key(cfg: config.Config, tag: str) -> str:
    """Get the key (or button) for the action"""
    hidconfig = cfg.config[tag].phasmo.hidconfig

    if isinstance(hidconfig, hidactions.KeyboardActionConfig):
        return hidconfig.key
    elif isinstance(hidconfig, hidactions.MouseButtonActionConfig):
        return hidconfig.button
    else:
        return KEY_IGNORED_STR


def get_command_text(cfg: config.Config, tag: str) -> str:
    """Get the command text for the action"""
    command_text = cfg.config[tag].twitch.command

    if isinstance(command_text, Iterable) and not isinstance(command_text, str):
        command_text = ", ".join(command_text)

    return command_text


def set_command_text(cfg: config.Config, tag: str, command_text: str) -> None:
    """Set the command text for the action"""
    cfg.config[tag].twitch.command = tuple(command.strip() for command in command_text.split(","))


def get_keybind_text(cfg: config.Config, tag: str) -> str:
    """Get the keybind text for the action"""
    keybind_text = cfg.config[tag].phasmo.hidconfig.key

    return keybind_text


def set_keybind_text(cfg: config.Config, tag: str, command_text: str) -> None:
    """Set the keybind text for the action"""
    cfg.config[tag].phasmo.hidconfig.key = command_text.strip()


def get_button_text(cfg: config.Config, tag: str) -> str:
    """Get the button text for the action"""
    button_text = cfg.config[tag].phasmo.hidconfig.button

    return button_text


def set_button_text(cfg: config.Config, tag: str, command_text: str) -> None:
    """Set the button text for the action"""
    cfg.config[tag].phasmo.hidconfig.button = command_text.strip()


def set_enabled_state(tk_obj, tk_var, predicate: Callable[[Any], bool]) -> None:
    """Set the state of a Tk object based on a Tk variable and predicate"""
    tk_obj.configure(state=tk.NORMAL if predicate(tk_var.get()) else tk.DISABLED)


def get_hid_type_text(cfg: config.Config, tag: str) -> str:
    """Get the HID type text for the action"""
    hid_type_text = cfg.config[tag].phasmo.hidconfig.device.name

    return hid_type_text


def populate_frame(cfg: config.Config,
                   selection: tk.StringVar,
                   enabled: tk.BooleanVar,
                   key: tk.StringVar,
                   cooldown: tk.DoubleVar,
                   random_chance: tk.IntVar,
                   command: tk.StringVar,
                   key_entry: tk.Entry) -> None:
    """Populate the frame with the selected action"""
    enabled.set(cfg.config[selection.get()].twitch.enabled)

    key.set(get_key(cfg, selection.get()))

    set_enabled_state(key_entry, key, lambda x: x != KEY_IGNORED_STR)

    cooldown.set(cfg.config[selection.get()].twitch.cooldown)
    random_chance.set(cfg.config[selection.get()].twitch.random_chance)
    command.set(get_command_text(cfg, selection.get()))


def make_window(cfg: config.Config, width_px: int, height_px: int) -> tk.Tk:
    """Make the window"""
    window = tk.Tk()
    window.title(f"Simon Says {cfg.version} by DrGreenGiant")
    window.geometry(f"{width_px}x{height_px}")
    return window


def make_canvas(cfg: config.Config, image_path: str, updateavailable: semantic_version = None, *, window: tk.Tk | None = None) -> tk.Canvas:
    """Make the canvas with a background image"""
    # img = tk.PhotoImage(file=image_path)
    from PIL import Image
    width, height = Image.open(image_path).size

    window = window or make_window(cfg, width, height)
    img = tk.PhotoImage(file=image_path)

    canvas = tk.Canvas(window, width=img.width(), height=img.height())
    canvas.pack(expand=True, fill=tk.BOTH)

    canvas.create_image((0, 0), image=img, anchor=tk.N + tk.W)
    canvas.image = img  # Keep a reference to the image to prevent garbage collection
    channels = "\n".join(cfg.channel)
    canvas.create_text((5, 5), text=f"Connected to channels:\n{channels}", anchor=tk.N + tk.W)

    versiontext = f"Version: {cfg.version}"
    if updateavailable:
        versiontext += "\nNew version available!"
        versiontext += f"\nLatest version: {updateavailable}"

    canvas.create_text((img.width() - 5, 5), text=versiontext, anchor=tk.N + tk.E)

    window.update()

    return canvas


def make_selection_frame(where, cfg: config.Config) -> tuple[tk.Frame, tk.StringVar]:
    """Make the selection frame"""
    frame = tk.Frame(where, width=320, height=50, relief='raised', borderwidth=5)

    selection = tk.StringVar(where)
    selection.set(next(iter(cfg.config)))

    tk.Label(frame, text="Select action:").pack(side=tk.LEFT, anchor=tk.W, padx=10)
    tk.OptionMenu(frame, selection, *list(cfg.config.keys())).pack(side=tk.RIGHT, anchor=tk.E, padx=10)

    return frame, selection


def pack_lhs(thing: tk.Frame) -> None:
    """Pack to the left"""
    thing.pack(side=tk.LEFT, anchor=tk.W)
    # thing.pack_propagate(False)


def pack_rhs(thing: tk.Frame) -> None:
    """Pack to the right"""
    thing.pack(side=tk.RIGHT, anchor=tk.E)
    # thing.pack_propagate(False)


@dataclasses.dataclass(frozen=True, slots=True)
class RuntimeFrames:
    """Runtime frames"""
    root: tk.Tk
    cfg: config.Config
    selection: tk.StringVar
    frame_width: int

    def make_labelled_checkbox_frame(self, name: str, initial_value: bool, setter: Callable[[bool], None]) -> tuple[tk.Frame, tk.BooleanVar]:
        """Make a labelled checkbox frame"""
        frame = tk.Frame(self.root, width=self.frame_width, height=50)

        enabled = tk.BooleanVar(frame)
        enabled.set(initial_value)

        label = tk.Label(frame, text=name, width=25, anchor=tk.E)

        cb = functools.partial(Callbacks.set_var_cb,
                               self.cfg,
                               setter,
                               self.selection,
                               enabled)
        button = tk.Checkbutton(frame, width=25, onvalue=True, offvalue=False, variable=enabled, command=cb, anchor=tk.W)

        pack_lhs(label)
        pack_rhs(button)

        return frame, enabled

    def make_labelled_text_frame(self, name: str, initial_value: str, setter: Callable[[str], None], *, disabled: bool = False) -> tuple[tk.Frame, tk.StringVar]:
        """Make a labelled text frame"""
        frame = tk.Frame(self.root, width=self.frame_width, height=50)

        command = tk.StringVar(frame)
        command.set(initial_value)

        cb = functools.partial(Callbacks.set_key_cb,
                               self.cfg,
                               setter,
                               self.selection,
                               command)
        command.trace_add("write", cb)

        label = tk.Label(frame, text=name, width=25, anchor=tk.E)

        entry = tk.Entry(frame, width=33, textvariable=command, state=tk.DISABLED if disabled else tk.NORMAL)

        pack_lhs(label)
        pack_rhs(entry)

        return frame, command

    def make_dropdown_frame(self, name: str, initial_value: str, options: list[str], setter: Callable[[str], None] = None) -> tuple[tk.Frame, tk.StringVar]:
        """Make the command frame"""
        frame = tk.Frame(self.root, width=self.frame_width, height=50)

        value = tk.StringVar(frame)
        value.set(initial_value)

        label = tk.Label(frame, text=name, width=25, anchor=tk.E)

        dropdown = tk.OptionMenu(frame, value, *options)
        dropdown.config(width=27)

        pack_lhs(label)
        pack_rhs(dropdown)

        return frame, value

    def make_button_frame(self, name: str, initial_value: str, setter: Callable[[str], None] = None) -> tuple[tk.Frame, tk.StringVar]:
        """Make the command frame"""
        frame = tk.Frame(self.root, width=self.frame_width, height=50)

        value = tk.StringVar(frame)
        value.set(initial_value)

        label = tk.Label(frame, text=name, width=25, anchor=tk.E)

        button = tk.Button(frame, text=value.get())
        button.config(width=27, command=setter)

        pack_lhs(label)
        pack_rhs(button)

        return frame, value


def make_cooldown_frame(where, cfg: config.Config, selection: tk.StringVar, frame_width: int) -> tuple[tk.Frame, tk.IntVar]:
    """Make the cooldown frame"""
    frame = tk.Frame(where, width=frame_width, height=50)

    cooldown = tk.IntVar(frame)
    cooldown.set(cfg.config[selection.get()].twitch.cooldown)

    cb = functools.partial(Callbacks.set_cooldown_cb, cfg, selection, cooldown)

    label = tk.Label(frame, text="Cooldown", width=25, anchor=tk.E)
    # scale = tk.Label(frame, text="Cooldown", width=25, anchor=tk.W)
    scale = tk.Scale(frame, length=200, from_=0, to=300, resolution=1, orient=tk.HORIZONTAL, variable=cooldown, command=cb)

    pack_lhs(label)
    pack_rhs(scale)

    return frame, cooldown


def make_random_frame(where, cfg: config.Config, selection: tk.StringVar, frame_width: int) -> tuple[tk.Frame, tk.IntVar]:
    """Make the random frame"""
    frame = tk.Frame(where, width=frame_width, height=50)

    random_chance = tk.IntVar(frame)
    random_chance.set(cfg.config[selection.get()].twitch.random_chance)

    cb = functools.partial(Callbacks.set_random_chance_cb, cfg, selection, random_chance)

    label = tk.Label(frame, text="Random chance", width=25, anchor=tk.E)
    scale = tk.Scale(frame, length=200, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, variable=random_chance, command=cb)

    pack_lhs(label)
    pack_rhs(scale)

    return frame, random_chance


def set_enabled(cfg: config.Config, selection: tk.StringVar, state: bool) -> None:
    """Set the enabled state for the action"""
    cfg.config[selection.get()].twitch.enabled = state


@dataclasses.dataclass(slots=True)
class UpdateArgs:
    """Arguments for updating the GUI"""
    canvas: tk.Canvas
    cfg: config.Config
    option_frame: tk.Frame | None
    selection: tk.StringVar
    redraw: mp.Event


def make_option_frame(optionargs: UpdateArgs, *args) -> tuple[tk.Frame, dict]:
    """Make the option frame"""
    FRAME_WIDTH = 400

    frame = tk.Frame(optionargs.canvas, width=FRAME_WIDTH, height=200)
    runtimeframes = RuntimeFrames(frame, optionargs.cfg, optionargs.selection, FRAME_WIDTH)

    guivars = {}

    name = "Enabled"
    enabled_frame, var = runtimeframes.make_labelled_checkbox_frame(name,
                                                                    optionargs.cfg.config[optionargs.selection.get()].twitch.enabled,
                                                                    functools.partial(set_enabled, optionargs.cfg, optionargs.selection))
    enabled_frame.pack()
    guivars[name.lower()] = var

    name = "Command"
    command_frame, var = runtimeframes.make_labelled_text_frame(name,
                                                                get_command_text(optionargs.cfg, optionargs.selection.get()),
                                                                lambda state, cfg=optionargs.cfg, selection=optionargs.selection:
                                                                set_command_text(optionargs.cfg, optionargs.selection.get(), state))
    command_frame.pack()
    guivars[name.lower()] = var

    # if not cfg.actions[selection.get()].action.chained:
    #     name = "Action type"
    #     action_type_frame, var = runtimeframes.make_dropdown_frame(name,
    #                                                                get_hid_type_text(cfg, selection.get()),
    #                                                                [hidtype.name for hidtype in hidactions.HidType])
    #     action_type_frame.pack()
    #     guivars[name.lower()] = var

    if not optionargs.cfg.actions[optionargs.selection.get()].action.chained:
        def on_press(key: hidactions.Key | hidactions.Button, tag: str, triggerredraw: mp.Event) -> None:
            """On press"""
            hidactions.stop_listeners()
            print(f"Pressed {key} for action {tag}")

            if isinstance(key, hidactions.Key):
                print(f"Setting keybind to {key.name}")
                new_hidconfig = hidactions.KeyboardActionConfig(key=key.name)
                optionargs.cfg.actions[tag].action.config.hidconfig = new_hidconfig
                optionargs.cfg.save()
            elif isinstance(key, hidactions.KeyCode):
                print(f"Setting keybind to {key.char}")
                new_hidconfig = hidactions.KeyboardActionConfig(key=key.char)
                optionargs.cfg.actions[tag].action.config.hidconfig = new_hidconfig
                optionargs.cfg.save()
            elif isinstance(key, hidactions.Button):
                print(f"Setting button to {key.name}")
                new_hidconfig = hidactions.MouseButtonActionConfig(button=key.name)
                optionargs.cfg.actions[tag].action.config.hidconfig = new_hidconfig
                optionargs.cfg.save()
            else:
                raise ValueError(f"Unknown key type: {key}")

            triggerredraw.set()

        callback = functools.partial(on_press, tag=optionargs.selection.get(), triggerredraw=optionargs.redraw)

        name = ""
        action_type_frame, var = runtimeframes.make_button_frame(name,
                                                                 "Set keybind",
                                                                 lambda: hidactions.start_listeners(callback))
        action_type_frame.pack()
        guivars[name.lower()] = var

    if isinstance(optionargs.cfg.config[optionargs.selection.get()].phasmo.hidconfig, hidactions.KeyboardActionConfig):
        name = "Keyboard"
        keybind_frame, var = runtimeframes.make_labelled_text_frame(name,
                                                                    get_keybind_text(optionargs.cfg, optionargs.selection.get()),
                                                                    lambda state, cfg=optionargs.cfg, selection=optionargs.selection:
                                                                    set_keybind_text(optionargs.cfg, optionargs.selection.get(), state))
        keybind_frame.pack()
        guivars[name.lower()] = var
    elif isinstance(optionargs.cfg.config[optionargs.selection.get()].phasmo.hidconfig, hidactions.MouseButtonActionConfig):
        name = "Mouse Button"
        button_frame, var = runtimeframes.make_labelled_text_frame(name,
                                                                   get_button_text(optionargs.cfg, optionargs.selection.get()),
                                                                   lambda state, cfg=optionargs.cfg, selection=optionargs.selection:
                                                                   set_button_text(optionargs.cfg, optionargs.selection.get(), state))
        button_frame.pack()
        guivars[name.lower()] = var

    cooldown_frame, cooldown = make_cooldown_frame(frame, optionargs.cfg, optionargs.selection, FRAME_WIDTH)
    cooldown_frame.pack()
    guivars['cooldown'] = cooldown

    random_chance_frame, random_chance = make_random_frame(frame, optionargs.cfg, optionargs.selection, FRAME_WIDTH)
    random_chance_frame.pack()
    guivars['random_chance'] = random_chance

    return frame, guivars


def update_from_selection(args: UpdateArgs, var, index, mode) -> None:
    """Update the vars from the selection"""
    window = args.canvas.winfo_toplevel()

    #  Remove callback on selection variable
    [args.selection.trace_remove(*trace) for trace in args.selection.trace_info()]

    if args.option_frame:
        args.option_frame.pack_forget()
        args.option_frame.destroy()
        args.option_frame = None

    args.option_frame, _ = make_option_frame(args)
    args.option_frame.pack(side=tk.TOP, anchor=tk.N, fill="none", pady=10, expand=True)
    args.option_frame.pack_propagate(False)

    args.selection.trace_add("write", functools.partial(update_from_selection, args))

    window.update()


def enabled_cb(cfg: config.Config, enabled_button: tk.Button, state_var: tk.BooleanVar) -> None:
    """Toggle the enabled state"""
    if state_var.get():
        # Currently on, turn off
        enabled_button.configure(text="Disabled", fg="black", bg="red")
        cfg.enabled = False
        state_var.set(False)
        print("Disabled")
    else:
        # Currently off, turn on
        enabled_button.configure(text="Enabled", fg="white", bg="green")
        cfg.enabled = True
        state_var.set(True)
        print("Enabled")


def make_gui(cfg: config.Config, updateavailable: semantic_version.Version = None) -> tuple[tk.Tk, mp.Event, Callable]:
    """Make the GUI"""
    canvas = make_canvas(cfg, environment.resource_path("assets", "Green_tato_640.png"), updateavailable)
    window = canvas.winfo_toplevel()

    triggerredraw = mp.Event()
    exit_event = mp.Event()
    window.protocol("WM_DELETE_WINDOW", functools.partial(on_closing, exit_event))

    selection_frame, selection = make_selection_frame(canvas, cfg)
    selection_frame.pack(side=tk.TOP, anchor=tk.N, pady=10, expand=True)

    redrawargs = UpdateArgs(canvas, cfg, None, selection, triggerredraw)
    selection.trace_add("write", functools.partial(update_from_selection, redrawargs))
    x = next(iter(cfg.config))
    selection.set(x)

    enabled_state = tk.BooleanVar(canvas)
    enabled_button = tk.Button(canvas, width=25)
    enabled_button.configure(command=functools.partial(enabled_cb, cfg, enabled_button, enabled_state))
    enabled_button.pack(side=tk.BOTTOM, anchor=tk.S, pady=10, expand=True)
    enabled_state.set(not cfg.enabled)  # Invoke will invert this var
    enabled_button.invoke()

    window.update()

    return window, exit_event, functools.partial(redraw, redrawargs)


def redraw(updateargs: UpdateArgs) -> None:
    """Redraw the GUI"""
    if updateargs.redraw.is_set():
        updateargs.redraw.clear()
        update_from_selection(updateargs, None, None, None)

    updateargs.canvas.update()
