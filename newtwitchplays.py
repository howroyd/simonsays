#!./.venv/bin/python3
import concurrent.futures as cf
import functools
import pprint

import phasmoactions as pa
import twitchactions as ta


def done_callback(future, command):
    print(f"Done: {command.tag=}")


if __name__ == "__main__":
    print("Hello World!")

    keybinds = pa.make_default_keybinds()
    keybinds["walk_forward"] = "up"
    keybinds["crouch"] = "ctrl"
    config = pa.Config(keybinds=keybinds)

    phasmoActions = pa.make_action_list(config)
    pprint.pprint(phasmoActions)

    print()

    with cf.ThreadPoolExecutor(max_workers=1) as executor:

        while True:
            command = input("Enter a command: ").lower()

            action = ta.find_command(phasmoActions, command)

            print(f"{command=}: {action.__class__=}\n")

            if action is not None:
                future = executor.submit(action.run)
                future.add_done_callback(functools.partial(done_callback, command=action))
