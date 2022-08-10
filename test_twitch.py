import time
import twitch

CHANNEL = "katatouille93"

def test_channel_connection() -> bool:
    with twitch.ChannelConnection(CHANNEL) as tw:
        t_start = time.time()
        for i in range(5):
            tw.run()
            if tw.last_ping and tw.last_ping > t_start:
                return True
            time.sleep(1)
    return False

if __name__ == "__main__":
    ret = False
    
    for i in range(3):
        try:
            ret = test_channel_connection()
            if ret:
                break
        except Exception as e:
            print(e)
        
    assert(ret)