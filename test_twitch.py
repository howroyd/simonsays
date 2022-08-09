import twitch

CHANNEL = "katatouille93"

def test_channel_connection():
    with twitch.ChannelConnection(CHANNEL) as tw:
        tw.run()
        assert(True)

if __name__ == "__main__":
    test_channel_connection()
            