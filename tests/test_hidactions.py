import pytest

from simonsays_drgreengiant import hidactions


def test_str_to_button():
    """Test str_to_button"""
    assert hidactions.Button.left == hidactions.str_to_button("left")
    assert hidactions.Button.middle == hidactions.str_to_button("middle")
    assert hidactions.Button.right == hidactions.str_to_button("right")

    with pytest.raises(hidactions.ButtonUnknown):
        hidactions.str_to_button("unknown")


def test_mousemovedirection():
    """Test MouseMoveDirection"""
    assert hidactions.MouseMoveDirection.UP == hidactions.MouseMoveDirection("up")
    assert hidactions.MouseMoveDirection.DOWN == hidactions.MouseMoveDirection("down")
    assert hidactions.MouseMoveDirection.LEFT == hidactions.MouseMoveDirection("left")
    assert hidactions.MouseMoveDirection.RIGHT == hidactions.MouseMoveDirection("right")

    with pytest.raises(hidactions.MouseMoveDirectionUnknown):
        hidactions.MouseMoveDirection("unknown")

    distance = 10
    assert (0, -distance) == hidactions.MouseMoveDirection.to_cartesian(hidactions.MouseMoveDirection.UP, distance)
    assert (0, distance) == hidactions.MouseMoveDirection.to_cartesian(hidactions.MouseMoveDirection.DOWN, distance)
    assert (-distance, 0) == hidactions.MouseMoveDirection.to_cartesian(hidactions.MouseMoveDirection.LEFT, distance)
    assert (distance, 0) == hidactions.MouseMoveDirection.to_cartesian(hidactions.MouseMoveDirection.RIGHT, distance)
    assert (0, -distance) == hidactions.MouseMoveDirection.to_cartesian("up", distance)
    assert (0, distance) == hidactions.MouseMoveDirection.to_cartesian("down", distance)
    assert (-distance, 0) == hidactions.MouseMoveDirection.to_cartesian("left", distance)
    assert (distance, 0) == hidactions.MouseMoveDirection.to_cartesian("right", distance)
