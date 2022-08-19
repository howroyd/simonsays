import logging
import time
import twitch

def channel_connection(channel: str) -> bool:
    timeout_s = 15

    with twitch.ChannelConnection(channel) as tw:
        return True
    return False # FIXME Throws if failed, so False is unreachable making this code wrong.

def test_channel_connection(n_retries: int = 4) -> bool:
    ret = False

    for i in range(n_retries):
        try:
            if channel_connection("katatouille93"):
                return True
        except Exception as e:
            print(e)
            time.sleep(1)

    return False

if __name__ == "__main__":
    assert test_channel_connection(), "test_channel_connection failed"
    print("Passed")