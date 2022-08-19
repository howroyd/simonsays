import keymap, default_config
from configparser import ConfigParser

def make_testing_config_dict() -> dict[str, dict[str, str]]:
    return {
        default_config.ConfigKeys.keyboard:     {
            "forward":      "w",
        },
        default_config.ConfigKeys.mouse_config: {
            "distance":     "500",
        },
        default_config.ConfigKeys.mouse:        {
            "lmb":          "lmb",
        },
    }

def test_make_keymap_entry() -> bool:
    cfg = make_testing_config_dict()
    parsed = keymap.make_keymap_entry(cfg)

    if len(parsed) == 2:
        return True
    return False

if __name__ == "__main__":
    assert test_make_keymap_entry(), "make_keymap_entry failed"
    print("Passed")