#!./.venv/bin/python3
import copy
import dataclasses

import tomlkit

import phasmoactions as pa  # TODO coupling to this module
import twitchactions as ta

FILENAME = "runtime.toml"
IGNORE_MEMBERS = ['tag', 'config', 'last_used', 'chained']


@dataclasses.dataclass
class Runtime:
    """Runtime data container"""
    version: str
    channel: str
    action_list: ta.TwitchActionList
    runtime_dict: ta.TwitchRuntimeDict
    config: pa.Config


def merge_interesting_data(runtime: Runtime) -> dict:
    """Merge the interesting runtime data into a dict"""
    asdict = {}
    for k, v in runtime.runtime_dict.items():
        asdict[k] = dataclasses.asdict(v)
    #asdict = {k: v.to_dict() for k, v in runtime.runtime_dict.items()}
    mycopy = copy.deepcopy(asdict)

    for tag, command in mycopy.items():
        action = next((x for x in runtime.action_list if x.tag == tag), None)
        if action:
            for subtag, val in dataclasses.asdict(action).items():
                asdict[tag][subtag] = val

    mycopy = copy.deepcopy(asdict)
    for tag, command in mycopy.items():
        action = next((x for x in runtime.action_list if x.tag == tag), None)
        for k, v in command.items():
            if (v is None) or (k in IGNORE_MEMBERS) or (k.startswith(('key', 'button')) and action.chained):
                asdict[tag].pop(k)

    asdict['channel'] = runtime.channel
    asdict['version'] = runtime.version

    return asdict


def save_config(runtime: Runtime) -> None:
    """Save the config to file"""
    towrite = merge_interesting_data(runtime)

    with open(FILENAME, "w") as f:
        s = tomlkit.dumps(towrite)
        f.write(s)
