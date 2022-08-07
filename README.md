# TwitchPlays
This work in progress code is a tidy up of an excellent system seen on DoudDougW's Twitch channel (https://www.twitch.tv/dougdougw)

They've kindly provided the code on their website (https://www.dougdoug.com/twitchplays)

I was unable to find the work on github, so created a fresh repository.  If anyone knows otherwise, please let me know so I can attribute this repo to their work in the usual github way.

The initial commit on `main` whows the original files as taken from the website when I started this.  The original header is at the bottom of this readme.  I've added a GNU GPL v2 as I believe this license matches the header comments and way the code has been distributed before me.  Any issues, please do let me know.

# Windows Defender
In the releases section of this repository are `exe` files you can download and try.  For now they are hard coded to a particular channel, I will sort that out in the future.  If you do download this `exe`, Windows Defender will throw a fit.  Feel free to Google "pyinstaller windows defender" to see what the issue is with needing to pay for a certificate, which I can't justify for free software.

So you have a few options:
- Disable Windows Defender; Hell no.  Don't do this.  Anyone who tells you to is either an idiot, dangerous or both.
- Go into Windows Defender, look at the history, and allow this `exe` that it had blocked.
- Don't use the `exe`; instead run the raw Python (see below)

I am not hating on Defender really.  This code opens connections over the internet, sends and receives data and initiates HID (keyboard and mouse) commands.  It looks exactly like many Trojans.  It is only you the human that can decide whether it is malicious or not, hopefully you can see all the information here to inform that decision.

## Running the raw Python
Many tutorials on the internet on how to get Python.  I am using v3.10.  Eventually I might make a `requirements.txt` to make the process of getting dependencies easier.  I don't think I am using any libraries not already packaged with Python so I think it is good.  I will check this another day though.

The only difference between running the `exe` or running the Python, is that the `exe` does not require the host machine to have Python installed.  I assume most broadcasters don't use Python, don't care about it and don't want to install loads of extra stuff on their machines.  The `exe` is also more portable as it doesn't care if you do already have Python installed, but the wrong version, missing dependencies, etc.  However, it is less portable because of Windows Defender flagging this.

## Building your own exe
There is a batch script, `create_exe.bat` which you can run from a cmd window to build the `exe`.  This is what I use and I have included it in the repo for visibility for those concerned about the above security issues.

You will see that in the batch script there is a link to a `png` image to use as the `exe` icon.  This is image file is NOT included in this repo as I do not own the rights to distribute it as an image, but I am permitted by _katatouille93_ to use it embedded inside the `exe` for the icon.  You can just remove the `-i <image_file>` from the script, or change `<filename>` to an image of your choosing.

You have all the source and also the mechanism to build the `exe` I put in the Releases section of this repo.  It is up to you to exercise due diligence as to whether you trust this process enough to make exceptions in Windows Defender.

## Suggestions or Queries
If you have any suggestions, questions or concerns, then please do use the appropriate features of Github (issues and discussions) to get in touch.

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