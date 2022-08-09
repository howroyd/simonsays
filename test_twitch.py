import twitch

CHANNEL = "katatouille93"

def test_channel_connection() -> bool:
    with twitch.ChannelConnection(CHANNEL) as tw:
        tw.run()
        return True
    return False

if __name__ == "__main__":
    ret = False
    
    for i in range(3):
        try:
            ret = test_channel_connection()
            if ret:
                print(f"Test success, connected to {CHANNEL}")
                assert(ret)
                exit()
        except Exception as e:
            print(e)
        
    assert(ret)