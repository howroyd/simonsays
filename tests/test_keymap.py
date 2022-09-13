import keymap, default_config
from configparser import ConfigParser
import pytest

@pytest.fixture
def good_keymap() -> dict[str, dict[str, str]]:
    return {
        default_config.ConfigKeys.keyboard:     {
            "talk":                 "v",
            "forward, forwards":    "w 3"
        },
        default_config.ConfigKeys.mouse_config: {
            "distance":             "500",
        },
        default_config.ConfigKeys.mouse:        {
            "lmb":                  "lmb",
            "look right":           "right"
        },
    }

def test_make_keymap_entry(good_keymap: dict[str, dict[str, str]]) -> None:
    parsed = keymap.make_keymap_entry(good_keymap)

    assert len(parsed) == 4, "make_keymap_entry failed"

@pytest.fixture
def bad_keyboard_keymap() -> dict[str, dict[str, str]]:
    return {
        default_config.ConfigKeys.keyboard:     {
            "talk":                 "v",
            "forward, forwards":    ""
        },
        default_config.ConfigKeys.mouse_config: {
            "distance":             "500",
        },
        default_config.ConfigKeys.mouse:        {
            "lmb":                  "lmb",
            "look right":           "right"
        },
    }

def test_make_keymap_entry_bad_keyboard(bad_keyboard_keymap: dict[str, dict[str, str]]) -> None:
    with pytest.raises(ValueError):
        keymap.make_keymap_entry(bad_keyboard_keymap)

@pytest.fixture
def bad_mouse_keymap() -> dict[str, dict[str, str]]:
    return {
        default_config.ConfigKeys.keyboard:     {
            "talk":                 "v",
            "forward, forwards":    "w 3"
        },
        default_config.ConfigKeys.mouse_config: {
            "distance":             "500",
        },
        default_config.ConfigKeys.mouse:        {
            "lmb":                  "invalid",
            "look right":           "right"
        },
    }

def test_make_keymap_entry_bad_mouse(bad_mouse_keymap: dict[str, dict[str, str]]) -> None:
    with pytest.raises(ValueError):
        keymap.make_keymap_entry(bad_mouse_keymap)