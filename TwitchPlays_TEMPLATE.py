# Written by DougDoug and DDarknut

# Hello! This file contains the main logic to process Twitch chat and convert it to game commands.
# The code is written in Python 3.X
# There are 2 other files needed to run this code:
    # TwitchPlays_KeyCodes.py contains the key codes and functions to press keys in-game. You should not modify this file.
    # TwitchPlays_Connection.py is the code that actually connects to Twitch. You should not modify this file.

# The source code primarily comes from:
    # Wituz's "Twitch Plays" tutorial: http://www.wituz.com/make-your-own-twitch-plays-stream.html
    # PythonProgramming's "Python Plays GTA V" tutorial: https://pythonprogramming.net/direct-input-game-python-plays-gta-v/
    # DDarknut's message queue and updates to the Twitch networking code

# Disclaimer: 
    # This code is NOT intended to be professionally optimized or organized.
    # We created a simple version that works well for livestreaming, and I'm sharing it for educational purposes.

##########################################################

TWITCH_CHANNEL = 'dougdougw' # Replace this with your Twitch username. Must be all lowercase.

##########################################################

import keyboard
import TwitchPlays_Connection
import pydirectinput
import random
import pyautogui
import concurrent.futures
from TwitchPlays_KeyCodes import *

##########################################################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 20  
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

##########################################################

# An optional count down before starting, so you have time to load up the game
countdown = 10
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

t = TwitchPlays_Connection.Twitch();
t.twitch_connect(TWITCH_CHANNEL);

def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        print("Got the message: [" + msg + "] from user [" + username + "]")

        # Now that you have a chat message, this is where you add your game logic.
        # Use the "HoldKey(KEYCODE)" function to press and hold down a keyboard key.
        # Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
        # Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
        # Use the pydirectinput library to press or move the mouse

        # I've added some example videogame logic code below:

        ###################################
        # Example GTA V Code 
        ###################################

        # If the chat message is "left", then hold down the A key for 2 seconds
        if msg == "left": 
            HoldAndReleaseKey(A, 2)

        # If the chat message is "right", then hold down the D key for 2 seconds
        if msg == "right": 
            HoldAndReleaseKey(D, 2)

        # If message is "drive", then permanently hold down the W key
        if msg == "drive": 
            ReleaseKey(S) #release brake key first
            HoldKey(W) #start permanently driving

        # If message is "reverse", then permanently hold down the S key
        if msg == "reverse": 
            ReleaseKey(W) #release drive key first
            HoldKey(S) #start permanently reversing

        # Release both the "drive" and "reverse" keys
        if msg == "stop": 
            ReleaseKey(W)
            ReleaseKey(S)

        # Press the spacebar for 0.7 seconds
        if msg == "brake": 
            HoldAndReleaseKey(SPACE, 0.7)

        # Press the left mouse button down for 1 second, then release it
        if msg == "shoot": 
            pydirectinput.mouseDown(button="left")
            time.sleep(1)
            pydirectinput.mouseUp(button="left")

        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))


while True:

    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages();
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time();

    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        exit()

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
