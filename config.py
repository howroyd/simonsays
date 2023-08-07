#!./.venv/bin/python3
import copy
import dataclasses
import enum

import tomlkit

import phasmoactions
import twitchactions

FILENAME = "config.toml"
DEFAULT_CHANNEL = "drgreengiant"


@dataclasses.dataclass(slots=True)
class ActionConfig:
    """The global config for TwitchPlays actions"""
    phasmo: phasmoactions.PhasmoActionConfig
    twitch: twitchactions.TwitchActionConfig


ConfigDict = dict[str, ActionConfig]


@dataclasses.dataclass(slots=True)
class Config:
    """The global config for TwitchPlays"""
    config: ConfigDict
    version: str
    channel: str = DEFAULT_CHANNEL
    filename: str = FILENAME

    def to_dict(self) -> dict:
        """Convert the config to a dict"""
        return {key: dataclasses.asdict(item) for key, item in self.config.items()}

    @staticmethod
    def replace_enum(config: dict) -> dict:
        """Replace enums with their values"""
        def _replace_enum(obj):
            """Replace enums with their values"""
            if isinstance(obj, dict):
                return {k: _replace_enum(v) for k, v in obj.items()}
            if isinstance(obj, enum.Enum):
                return obj.name
            return obj
        return {key: {k: _replace_enum(v) for k, v in item.items()} for key, item in config.items()}

    @staticmethod
    def remove_none(config: dict) -> dict:
        """Remove keys containing None values"""
        def _remove_none(obj):
            """Remove None values"""
            if isinstance(obj, dict):
                return {k: _remove_none(v) for k, v in obj.items() if v is not None}
            return obj
        return {key: _remove_none(item) for key, item in config.items()}

    def to_toml(self) -> str:
        """Convert the config to TOML"""
        asdict = self.to_dict()
        asdict = self.replace_enum(asdict)
        asdict = self.remove_none(asdict)

        return tomlkit.dumps(asdict | {"version": self.version, "channel": self.channel})

    def save(self) -> None:
        """Save the config to file"""
        towrite = self.to_toml()

        with open(self.filename, "w") as f:
            f.write(towrite)

    @classmethod
    def load(cls, filename: str = None) -> dict:
        """Load the config from file"""
        tomldata: tomlkit.document.TOMLDocument = None
        filename = filename or FILENAME

        with open(filename, "r") as f:
            tomldata = tomlkit.loads(f.read())

        actionstoml = {key: item for key, item in tomldata.items() if key != "version" and key != "channel"}
        phasmotoml = {key: item["phasmo"] for key, item in actionstoml.items()}
        twitchtoml = {key: item["twitch"] for key, item in actionstoml.items()}

        twitch = twitchactions.Config({key: twitchactions.TwitchActionConfig(**item) for key, item in twitchtoml.items()})
        phasmo = phasmoactions.from_toml(phasmotoml)

        return cls({key: ActionConfig(phasmo=phasmo.config[key], twitch=twitch.config[key]) for key, item in phasmotoml.items()},
                  version=tomldata["version"],
                  channel=tomldata["channel"],
                  filename=filename
                  )


def make_config(*, version: str, channel: str = None, phasmo: phasmoactions.Config = None, twitch: twitchactions.Config = None, filename: str = None) -> ConfigDict:
    """Make a config"""
    channel = channel or DEFAULT_CHANNEL
    phasmo = phasmo or phasmoactions.default_config()
    twitch = twitch or twitchactions.Config()
    filename = filename or FILENAME

    for key in phasmo.config.keys():
        if not key in twitch.config:
            twitch.config[key] = twitchactions.TwitchActionConfig(key)  # FIXME using the key as the command for now

    assert all(key in twitch.config for key in phasmo.config.keys())

    return Config({key: ActionConfig(phasmo=phasmo.config[key], twitch=twitch.config[key]) for key in phasmo.config.keys()},
                  version=version,
                  channel=channel,
                  filename=filename)
