import os
from configparser import ConfigParser
import default_config

def chack_keys_in_config(cfg: ConfigParser) -> bool:
    keys = list(default_config.ConfigKeys.as_dict().values())
    if all(key in cfg for key in keys):
        return True
    return False

def test_generate_default_config() -> bool:
    cfg = default_config.generate_default_config()
    return chack_keys_in_config(cfg)

def test_get_from_file() -> bool:
    filename = "test_config.ini"
    if os.path.isfile(filename):
        os.remove(filename)
    cfg = default_config.get_from_file(filename)
    ret = chack_keys_in_config(cfg)
    os.remove(filename)
    return ret

if __name__ == "__main__":
    assert test_generate_default_config(), "generate_default_config failed"
    assert test_get_from_file(), "test_get_from_file failed"
    print("Passed")