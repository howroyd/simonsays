#!./.venv/bin/python3
import dataclasses
from typing import Any, Callable, Protocol, Self

from . import errorcodes, hidactions


@dataclasses.dataclass(slots=True)
class ActionConfig(Protocol):
    """A config for a Phasmophobia action"""
    hidconfig: hidactions.Config

    @property
    def duration(self) -> float | None:
        """Get the duration"""
        ...

    @property
    def pause(self) -> float | None:
        """Get the pause"""
        ...

    @property
    def repeats(self) -> int | None:
        """Get the repeats"""
        ...

    @property
    def mousemovedirection(self) -> hidactions.MouseMoveDirection | None:
        """Get the mouse move direction"""
        ...

    @property
    def distance(self) -> int | None:
        """Get the distance"""
        ...


ConfigDict = dict[str, ActionConfig]


@dataclasses.dataclass(slots=True)
class Config:
    """The global config for all game actions"""
    config: ConfigDict = dataclasses.field(default_factory=ConfigDict)

    def __getitem__(self, name: str) -> ActionConfig | None:
        """Look up an action config"""
        return self.config.get(name, None)

    @classmethod
    def from_toml(cls, existing: dict[str, dict[str, Any]], *, default: Self | None = None) -> Self:
        """Get a config from an existing config"""
        ret = default or {}
        for key in ret.config.keys():
            if key in existing:
                to_replace = ret.config[key]
                using_this = existing.get(key, None)
                if using_this:
                    to_replace_hidconfig = to_replace.hidconfig
                    using_this_hidconfig = using_this.get("hidconfig", None)
                    kwargs = {**using_this}
                    if to_replace_hidconfig:
                        kwargs["hidconfig"] = type(to_replace.hidconfig)(**using_this_hidconfig) if using_this_hidconfig else to_replace.hidconfig
                        kwargs["hidconfig"].device = hidactions.HidType[kwargs["hidconfig"].device]
                    else:
                        kwargs["hidconfig"] = None
                    ret.config[key] = type(to_replace)(**kwargs)
        return ret


ConfigFn = Callable[[], Config]

#####################################################################


@dataclasses.dataclass(slots=True, kw_only=True)
class Action(hidactions.HidAction, Protocol):
    """Base class for Phasmophobia actions"""
    config_fn: ConfigFn
    name: str
    chained: bool

    @property
    def config(self) -> ActionConfig | None:
        """Get the config for this action"""
        ...


ActionDict = dict[str, Action]


@dataclasses.dataclass(slots=True)
class GenericActionBase:
    """Generic Phasmophobia action base class"""
    config_fn: ConfigFn

    @property
    def config(self) -> ActionConfig | None:
        """Get the config for this action"""
        return self.config_fn()[self.name]  # TODO: think about relying on self.name existing in child class


@dataclasses.dataclass(slots=True)
class GenericAction(GenericActionBase):
    """Generic Phasmophobia action"""

    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        """Run the action"""
        actionconfig: ActionConfig = self.config

        if not actionconfig:
            return errorcodes.errorset(errorcodes.ErrorCode.LOOKUP_FAILURE)

        if isinstance(actionconfig.hidconfig, hidactions.KeyboardActionConfig):
            return hidactions.PressReleaseKey(actionconfig.hidconfig).run(force=force)
        elif isinstance(actionconfig.hidconfig, hidactions.MouseButtonActionConfig):
            return hidactions.PressReleaseButton(actionconfig.hidconfig).run(force=force)
        elif isinstance(actionconfig.hidconfig, hidactions.MouseMoveCartesianActionConfig):
            return hidactions.MoveMouseRelative(actionconfig.hidconfig).run(force=force)
        elif isinstance(actionconfig.hidconfig, hidactions.MouseMoveDirectionActionConfig):
            return hidactions.MoveMouseRelativeDirection(actionconfig.hidconfig).run(force=force)
        else:
            return errorcodes.errorset(errorcodes.ErrorCode.NOT_IMPLEMENTED)

#####################################################################


@dataclasses.dataclass(slots=True)
class ActionAndConfig:
    """A pair of an action and config"""
    actiontype: type(Action)
    config: ActionConfig
    action: Action = dataclasses.field(init=False)

    def __post_init__(self):
        self.action = self.actiontype(lambda: self.config)


ActionAndConfigDict = dict[str, ActionAndConfig]
