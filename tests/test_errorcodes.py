import pytest
from simonsays_drgreengiant import errorcodes


def test_errorcodes():
    """Test that the error codes are correct."""
    assert errorcodes.ErrorCode.OK == 0
    assert errorcodes.ErrorCode.UNKNOWN == 1
    assert errorcodes.ErrorCode.NOT_IMPLEMENTED == 2
    assert errorcodes.ErrorCode.LOOKUP_FAILURE == 3
    assert errorcodes.ErrorCode.DISABLED == 4
    assert errorcodes.ErrorCode.ON_COOLDOWN == 5
    assert errorcodes.ErrorCode.RANDOM_CHANCE == 6
    assert errorcodes.ErrorCode.BLOCKED_USER == 7
    assert errorcodes.ErrorCode.BLOCKED_CHANNEL == 8


def test_errorset():
    """Test that errorset works as expected."""
    errors = errorcodes.errorset(errorcodes.ErrorCode.UNKNOWN)
    assert errors == {errorcodes.ErrorCode.UNKNOWN}

    errors = errorcodes.errorset([errorcodes.ErrorCode.UNKNOWN, errorcodes.ErrorCode.NOT_IMPLEMENTED])
    assert errors == {errorcodes.ErrorCode.UNKNOWN, errorcodes.ErrorCode.NOT_IMPLEMENTED}

    with pytest.raises(TypeError):
        errorcodes.errorset(1)


def test_success():
    """Test that success works as expected."""
    errors = errorcodes.ErrorCode.UNKNOWN
    assert not errorcodes.success(errorcodes.errorset(errors))

    errors = [errorcodes.ErrorCode.UNKNOWN, errorcodes.ErrorCode.NOT_IMPLEMENTED]
    assert not errorcodes.success(errorcodes.errorset(errors))

    errors = errorcodes.ErrorCode.OK
    assert errorcodes.success(errorcodes.errorset(errors))

    errors = [errorcodes.ErrorCode.OK, errorcodes.ErrorCode.OK]
    assert errorcodes.success(errorcodes.errorset(errors))
