#!./.venv/bin/python3
import dataclasses
import enum
import functools
import hashlib
import shutil
from typing import Callable, NoReturn, Self
from urllib.request import urlretrieve

import tomlkit

from . import (environment, errorcodes, gameactions, phasmoactions,
               twitchactions)

OFFLINE = environment.getenvboolean("OFFLINE", False)
NO_BLOCKLIST = environment.getenvboolean("NO_BLOCKLIST", OFFLINE)

DEFAULT_FILENAME = "config.toml"
DEFAULT_CHANNELS = {"drgreengiant"}
DEFAULT_SUPERUSERS = {"drgreengiant"}
DEFAULT_SUPERUSER_COMMAND_PREFIX = "sudo"
DEFAULT_BOTS = {"buttsbot", "streamelements", "nightbot", "streamlabs"}

BLOCKLIST = []
if not NO_BLOCKLIST:
    _f = open(urlretrieve("https://github.com/howroyd/twitchplays/releases/latest/download/blocklist")[0], "r")
    BLOCKLIST = _f.readlines()
    _f.close()
    del _f
del urlretrieve

# test = phasmoactions.PhasmoActions()


def check_blocklist(channel: str | set[str], *, abort: bool = True, silent: bool = False) -> list[str] | NoReturn:
    """Return any channels/users in the blocklist"""
    channels = channel if isinstance(channel, set) else set(channel)
    blockedchannels = [channel for channel in channels if hashlib.sha256(channel.strip().lower().encode("utf-8")).hexdigest() in BLOCKLIST]

    if blockedchannels:
        if not silent:
            print(f"User or Channel blocked: {', '.join(blockedchannels)}")
        if abort:
            exit(errorcodes.ErrorCode.BLOCKED_CHANNEL)

    return blockedchannels


@dataclasses.dataclass(slots=True)
class ActionConfig:
    """The global config for TwitchPlays actions"""
    phasmo: gameactions.ActionConfig
    twitch: twitchactions.TwitchActionConfig


ConfigDict = dict[str, ActionConfig]


@dataclasses.dataclass(slots=True)
class Config:
    """The global config for TwitchPlays"""
    config: ConfigDict
    version: str
    enabled: bool = True
    channel: set[str] = dataclasses.field(default_factory=lambda: DEFAULT_CHANNELS)
    superusers: set[str] = dataclasses.field(default_factory=lambda: DEFAULT_SUPERUSERS)
    superuser_prefix: str = DEFAULT_SUPERUSER_COMMAND_PREFIX
    bots: set[str] = dataclasses.field(default_factory=lambda: DEFAULT_BOTS)
    filename: str = DEFAULT_FILENAME
    actions: twitchactions.ActionDict = dataclasses.field(init=False, default_factory=dict)

    def __post_init__(self):
        self.channel = self.channel if isinstance(self.channel, set) else set(self.channel)
        self.superusers = self.superusers if isinstance(self.superusers, set) else set(self.superusers)
        self.bots = self.bots if isinstance(self.bots, set) else set(self.bots)
        check_blocklist(self.channel)

        actions = self._make_twitch_actions()
        randomaction, randomconfig = self._make_random_twitch_action(actions)
        actions.update(randomaction)

        self.config.update(randomconfig)
        self.actions = actions

    def find_tag_by_command(self, command: str) -> str | None:
        """Find a tag by command"""
        for key, action in self.actions.items():
            if action.check_command(command):
                return key
        return None

    @staticmethod
    def root_keys() -> set[str]:
        """Return the root keys"""
        return [
            "version",
            "enabled",
            "channel",
            "superusers",
            "superuser_prefix",
            "bots",
            "filename",
        ]

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
        asdict.pop("random")  # TODO this should maybe be a "dont_save" flag in the action config??
        asdict = self.replace_enum(asdict)
        asdict = self.remove_none(asdict)

        return tomlkit.dumps(asdict | {
            "version": self.version,
            "channel": list(self.channel),
            "superusers": list(self.superusers),
            "superuser_prefix": self.superuser_prefix,
            "bots": list(self.bots),
        })

    def save(self, *, backup_old: bool = False) -> None:
        """Save the config to file"""
        if backup_old:
            try:
                shutil.copyfile(self.filename, f"{self.filename}.bak")
            except FileNotFoundError as e:
                print(f"Could not backup old config file: {e}")

        towrite = self.to_toml()

        with open(self.filename, "w") as f:
            f.write(towrite)

    @classmethod
    def load(cls, version: str, filename: str = None) -> Self:
        """Load the config from file"""
        tomldata: tomlkit.document.TOMLDocument = None
        filename = filename or DEFAULT_FILENAME

        try:
            with open(filename, "r") as f:
                tomldata = tomlkit.loads(f.read())
        except FileNotFoundError:
            print(f"Config file not found: {filename=}")
        except tomlkit.exceptions.TOMLKitError as e:
            print(f"Error loading config file: {filename=}")
            print(e)

        actionstoml = {key: item for key, item in tomldata.items() if key not in cls.root_keys()} if tomldata else {}
        phasmotoml = {key: item["phasmo"] for key, item in actionstoml.items()} if actionstoml else {}
        twitchtoml = {key: item["twitch"] for key, item in actionstoml.items()} if actionstoml else {}

        phasmo = gameactions.Config.from_toml(phasmotoml, default=phasmoactions.default_config())
        twitch = twitchactions.from_toml(twitchtoml, phasmo.config.keys())

        assert all(key in twitch.config for key in phasmo.config.keys())

        channel = set(tomldata.get("channel", DEFAULT_CHANNELS)) if tomldata else DEFAULT_CHANNELS
        superusers = set(tomldata.get("superusers", DEFAULT_SUPERUSERS)) | DEFAULT_SUPERUSERS if tomldata else DEFAULT_SUPERUSERS
        # superusers = superusers | channel
        superuser_prefix = tomldata.get("superuser_prefix", DEFAULT_SUPERUSER_COMMAND_PREFIX) if tomldata else DEFAULT_SUPERUSER_COMMAND_PREFIX
        bots = set(tomldata.get("bots", DEFAULT_BOTS)) if tomldata else DEFAULT_BOTS

        return cls({key: ActionConfig(phasmo=phasmo.config[key], twitch=twitch.config[key]) for key in phasmo.config.keys()},
                   version=version,
                   channel=channel,
                   superusers=superusers,
                   superuser_prefix=superuser_prefix,
                   bots=bots,
                   filename=filename
                   )

    def _make_phasmo_actions(self) -> gameactions.ActionDict:
        """Make the phasmo actions"""
        return phasmoactions.all_actions_dict(lambda: gameactions.Config({key: item.phasmo for key, item in self.config.items()}))

    def _make_random_phasmo_action(self) -> phasmoactions.RandomAction:
        """Make a random phasmo action"""
        return phasmoactions.RandomAction(lambda: gameactions.Config({key: item.phasmo for key, item in self.config.items()}))

    def _get_twitch_config_fn(self) -> twitchactions.Config:
        """Get the twitch config"""
        return lambda: twitchactions.Config({key: item.twitch for key, item in self.config.items()})

    def _make_twitch_actions(self) -> twitchactions.ActionDict:
        """Make the twitch actions"""
        return {key: twitchactions.TwitchAction(self._get_twitch_config_fn(), key, value) for key, value in self._make_phasmo_actions().items()}

    def _make_random_twitch_action(self, existingactions: twitchactions.ActionDict) -> tuple[twitchactions.ActionDict, ConfigDict]:
        """Make a random twitch action"""
        random_action = self._make_random_phasmo_action()

        random_config = ActionConfig(
            phasmo=phasmoactions.RandomActionConfig(lambda: existingactions),
            twitch=twitchactions.TwitchActionConfig(random_action.name, random_chance=10)
        )

        twitchactiondict = {random_action.name: twitchactions.TwitchAction(self._get_twitch_config_fn(), random_action.name, random_action, force_underlying=True)}
        configdict = {random_action.name: random_config}

        return twitchactiondict, configdict

    def _make_superuser_actions(self, twitch_actions: twitchactions.ActionDict) -> dict[str, Callable]:
        """Make the superuser actions"""
        superuser_actions = {self.superuser_prefix + " " + key: functools.partial(value.run, force=True) for key, value in twitch_actions.items()}

        return {
            self.superuser_prefix + " reload": lambda: print("Reload!"),  # TODO
            self.superuser_prefix + " reset": lambda: [action.clear_cooldown() for action in twitch_actions.values()],
        } | superuser_actions
