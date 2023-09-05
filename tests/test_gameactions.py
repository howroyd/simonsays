import dataclasses

import pytest

from simonsays_drgreengiant import gameactions, hidactions, errorcodes


@dataclasses.dataclass(slots=True)
class Config:
    """A config for a Phasmophobia action"""
    duration: float = 0.1
    pause: float = 0.2
    repeats: int = 3
    mousemovedirection: hidactions.MouseMoveDirection = hidactions.MouseMoveDirection.UP
    distance: int = 10
    hidconfig: hidactions.Config = dataclasses.field(default_factory=lambda: hidactions.KeyboardActionConfig("x"))

    @property
    def duration(self) -> float | None:
        """Get the duration"""
        return self.duration

    @property
    def pause(self) -> float | None:
        """Get the pause"""
        return self.pause

    @property
    def repeats(self) -> int | None:
        """Get the repeats"""
        return self.repeats

    @property
    def mousemovedirection(self) -> hidactions.MouseMoveDirection | None:
        """Get the mouse move direction"""
        return self.mousemovedirection

    @property
    def distance(self) -> int | None:
        """Get the distance"""
        return self.distance


def test_getitem():
    """Test __getitem__"""
    testitem = {"test": Config()}
    config = gameactions.Config(testitem)
    assert config["test"] == testitem["test"]
    assert config["test2"] is None


@dataclasses.dataclass(slots=True)
class Action(gameactions.GenericAction):
    """A generic action"""
    name: str
    chained: bool


def test_genericaction():
    """Test GenericAction"""
    testitem = {"test": Config()}
    config = gameactions.Config(testitem)
    configfn: gameactions.ConfigFn = lambda: config
    genericaction = Action(configfn, "test", False)

    hidaction = hidactions.KeyboardActionConfig("x")
    testitem["test"].hidconfig = hidaction
    assert genericaction.config.hidconfig == hidaction
    assert errorcodes.success(genericaction.run()) is True

    hidaction = hidactions.MouseButtonActionConfig("left")
    testitem["test"].hidconfig = hidaction
    assert genericaction.config.hidconfig == hidaction
    assert errorcodes.success(genericaction.run()) is True

    # NOTE this test fails in headless Ubuntu
    # hidaction = hidactions.MouseMoveCartesianActionConfig(10, 20)
    # testitem["test"].hidconfig = hidaction
    # assert genericaction.config.hidconfig == hidaction
    # assert errorcodes.success(genericaction.run()) is True

    hidaction = hidactions.MouseMoveDirectionActionConfig(10, hidactions.MouseMoveDirection.UP)
    testitem["test"].hidconfig = hidaction
    assert genericaction.config.hidconfig == hidaction
    assert errorcodes.success(genericaction.run()) is True

    genericaction = Action(configfn, "testfail", False)
    assert genericaction.config is None
    retcode = genericaction.run()
    assert errorcodes.errorset(errorcodes.ErrorCode.LOOKUP_FAILURE) == retcode
    assert errorcodes.success(retcode) is False
