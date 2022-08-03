# TwitchPlays
This work in progress code is a tidy up of an excellent system seen on DoudDougW's Twitch channel (https://www.twitch.tv/dougdougw)

They've kindly provided the code on their website (https://www.dougdoug.com/twitchplays)

I was unable to find the work on github, so created a fresh repository.  If anyone knows otherwise, please let me know so I can attribute this repo to their work in the usual github way.

The initial commit on `main` whows the original files as taken from the website when I started this.  The original header is at the bottom of this readme.  I've added a GNU GPL v2 as I believe this license matches the header comments and way the code has been distributed before me.  Any issues, please do let me know.

---

# Original file header comments
> Written by DougDoug and DDarknut
> 
> Hello! This file contains the main logic to process Twitch chat and convert it to game commands.
> The code is written in Python 3.X
> There are 2 other files needed to run this code:
> - `TwitchPlays_KeyCodes.py` contains the key codes and functions to press keys in-game. You should not modify this file.
> - `TwitchPlays_Connection.py` is the code that actually connects to Twitch. You should not modify this file.
> 
> The source code primarily comes from:
> - Wituz's "Twitch Plays" tutorial: http://www.wituz.com/make-your-own-twitch-plays-stream.html
> - PythonProgramming's "Python Plays GTA V" tutorial: https://pythonprogramming.net/direct-input-game-python-plays-gta-v/
> - DDarknut's message queue and updates to the Twitch networking code
> 
> Disclaimer: 
> - This code is NOT intended to be professionally optimized or organized.
> - We created a simple version that works well for livestreaming, and I'm sharing it for educational purposes.