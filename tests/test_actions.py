import dataclasses

import pytest
from simonsays_drgreengiant import actions, errorcodes

WAIT_TIME = 0.01


@dataclasses.dataclass(slots=True)
class FailAction:
    def run(self, *, force: bool = False) -> errorcodes.ErrorSet:
        return errorcodes.errorset(errorcodes.ErrorCode.UNKNOWN)


def test_action_protocol():
    """Test Action protocol"""
    assert isinstance(FailAction(), actions.Action)


def test_action_repeat():
    """Test ActionRepeat"""
    action = actions.ActionRepeat(actions.Wait(WAIT_TIME), 3)
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.OK] * 3)

    action = actions.ActionRepeat(FailAction(), 3)
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN] * 3)


def test_action_sequence():
    """Test ActionSequence"""
    action = actions.ActionSequence([actions.Wait(WAIT_TIME), actions.Wait(WAIT_TIME), actions.Wait(WAIT_TIME)])
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.OK] * 3)

    action = actions.ActionSequence([FailAction(), FailAction(), FailAction()])
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN] * 3)


def test_wait():
    """Test Wait"""
    action = actions.Wait(WAIT_TIME)
    assert action.run() == errorcodes.errorset(errorcodes.ErrorCode.OK)


def test_wait_random():
    """Test WaitRandom"""
    action = actions.WaitRandom(WAIT_TIME, 2 * WAIT_TIME)
    assert action.run() == errorcodes.errorset(errorcodes.ErrorCode.OK)


def test_action_repeat_force():
    """Test ActionRepeat with force"""
    action = actions.ActionRepeat(actions.Wait(WAIT_TIME), 3)
    assert action.run(force=True) == errorcodes.errorset([errorcodes.ErrorCode.OK] * 3)

    action = actions.ActionRepeat(FailAction(), 3)
    assert action.run(force=True) == errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN] * 3)


def test_action_sequence_force():
    """Test ActionSequence with force"""
    action = actions.ActionSequence([actions.Wait(WAIT_TIME), actions.Wait(WAIT_TIME), actions.Wait(WAIT_TIME)])
    assert action.run(force=True) == errorcodes.errorset([errorcodes.ErrorCode.OK] * 3)

    action = actions.ActionSequence([FailAction(), FailAction(), FailAction()])
    assert action.run(force=True) == errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN] * 3)


def test_wait_force():
    """Test Wait with force"""
    action = actions.Wait(WAIT_TIME)
    assert action.run(force=True) == errorcodes.errorset(errorcodes.ErrorCode.OK)


def test_wait_random_force():
    """Test WaitRandom with force"""
    action = actions.WaitRandom(WAIT_TIME, 2 * WAIT_TIME)
    assert action.run(force=True) == errorcodes.errorset(errorcodes.ErrorCode.OK)


def test_action_repeat_with_wait():
    """Test ActionRepeatWithWait"""
    action = actions.ActionRepeatWithWait(actions.Wait(WAIT_TIME), 3, actions.Wait(WAIT_TIME))
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.OK] * 6)

    action = actions.ActionRepeatWithWait(FailAction(), 3, actions.Wait(WAIT_TIME))
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN, errorcodes.ErrorCode.OK] * 3)

    action = actions.ActionRepeatWithWait(FailAction(), 3, actions.WaitRandom(WAIT_TIME, 2 * WAIT_TIME), recalculate_wait=True)
    assert action.run() == errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN, errorcodes.ErrorCode.OK] * 3)

    with pytest.raises(ValueError):
        actions.ActionRepeatWithWait(FailAction(), 3, actions.Wait(WAIT_TIME), recalculate_wait=True)
