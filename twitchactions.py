#!./.venv/bin/python3
import dataclasses
import random

import hidactions


@dataclasses.dataclass(slots=True)
class TwitchAction(actions.Action):
    command: str | list[str]
    action: hidactions.HidAction

    def check_command(self, command: str) -> bool:
        '''Check if the command matches'''
        command = command.lower().lstrip().rstrip()

        if isinstance(self.command, str):
            return command.startswith(self.command)

        for command_ in self.command:
            if command.startswith(command_):
                return True

        return False

    def run(self) -> None:
        '''Run the action'''
        self.action.run()
