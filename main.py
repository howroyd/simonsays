VERSION = 0.1

import logging
from time import sleep
from keymap import iomap, emotemap

import twitch

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%y%m%d %H:%M:%S")

START_KEY: str = "shift+backspace"
STOP_KEY:  str = None # None means, s

test_keys = [
    "lmb",
    "left",
    "spin",
    "bollocks",
    "mmb",
    "rmb",
]

class TwitchAPI:
    def __init__(self, channel: str):
        logging.debug("Instantiating Twitch API connection to %s", channel)
        self.channel = channel
        self.impl = twitch.Twitch()
        self.impl.twitch_connect(self.channel)
        
    def receive(self):
        return self.impl.twitch_receive_messages()


def print_preamble(start_key: str, stop_key: str = None):
    if not stop_key:
        stop_key = start_key
        
    print("\TwitchPlays")
    print("Version", VERSION, "\n")
    
    print("For more info visit:")
    print("https://github.com/howroyd/twitchplays\n")
    
    print("To start press", start_key)
    print("To stop press",  stop_key)
    
    print("\n")

if __name__ == "__main__":
    
    print_preamble(START_KEY, STOP_KEY)    
    
    pkt = b'JOIN Hello world'
    
    x = twitch.TwitchMessage.from_bytes(pkt)
    print(x)
    
    with twitch.ChannelConnection("katatouille93") as tw:
        while True:
            tw.run()
            print(tw.get_all())
            sleep(1)

    #conn = TwitchAPI("eldel_")
    #conn = TwitchAPI("katatouille93")
    conn = TwitchAPI("veekaytv")
    
    # for msg in test_keys:
    #     try:
    #         fn, params = iomap[msg]
    #         fn(*params)
    #         sleep(1)
    #     except KeyError:
    #         logging.debug("Ignoring %s", msg)
    #         pass
        
    while True:
        new_messages = conn.receive();
        
        if (new_messages):
            for msg in new_messages:
                first_word = msg['message'].split()[0]
                try:
                    fn, params = emotemap[first_word]
                    fn(*params)
                    #sleep(1)
                except TypeError as e:
                    logging.error("Key %s threw %s", first_word, e)
                except KeyError:
                    pass
        
        sleep(0.1)