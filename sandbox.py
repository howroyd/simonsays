from typing import Any, Optional, Callable

def mouse_click(button: str):
    print(f"Mouse click {button}")

def key_press(key: str):
    print(f"Key press {key}")

def key_press_hold(key: str, duration: str):
    t = float(duration)
    print(f"Key hold {key} for {t}")

config = {
    "commands" : {
        "click" : "lmb",
        "forward, forwards" : "w 3",
        "back, backward, backwards" : "s 3",
        "strafe right" : "d 3",
        "nudge forward" : "w",
    }
}

mouse_commands = {
    "lmb": "left",
    "mmb": "middle",
    "rmb": "right"
}

Command = tuple[str, ...]
Action = tuple[Callable, tuple[str, ...]]
CommandAction = tuple[Command, Action]

def split_command_action(config_command: tuple[str, str]) -> CommandAction:
    command = tuple([x.lstrip().rstrip() for x in config_command[0].split(',')])
    action  = tuple(config_command[1].split())

    if any(action[0].startswith(key) for key in mouse_commands.keys()):
        return (command, (mouse_click, *action))

    if len(action) > 1:
        return (command, (key_press_hold, *action))

    return (command, (key_press, *action))

command_actions = []

for kv in config["commands"].items():
    command_actions.append(split_command_action(kv))

#for x in command_actions:
#    print(x)

chat_messages = [
    "nudge forward",
    "hello",
    "forwards",
    "hello",
    "back",
    "backwards",
    "click",
    "hello",
    "strafe",
    "hello",
    "strafe right",
    "hello",
]

def find_command_action(msg: str) -> Optional[CommandAction]:
    if not msg:
        return None

    for command_action in command_actions:
        if any(msg.startswith(s) for s in command_action[0]):
            return command_action

    return None

for msg in chat_messages:
    command_action = find_command_action(msg)
    #print(f"{msg}: {command_action}")
    if command_action:
        command, action = command_action
        action[0](*action[1:])