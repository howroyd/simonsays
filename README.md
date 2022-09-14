# Who am I?
Hi, I am Simon.  You might know me on Twitch as `GreenaGiant`.

My day job is as a senior embedded firmware engineer in the UK.  Normally writing C++ for bare metal devices, previously working in healthcare and also in construction.

I use Python regularly to create tools to help with work, and used it extensively in my PhD and postdoc.  I am pretty good at Python but I probably fall sort of being a Python professional, or maybe I am being too modest.

# Naming
I am not content with the name "TwitchPlays".   There are loads of other bits of software with this name.  Not only do I not wish to tread on their toes, it would also be nice to have a more unique identity.

If you have any suggestions, then please submit it in the `issues` tab, or create a `discussion`.  All ideas are greatly received and will of course be fully accredited.

# TwitchPlays
Example here: https://clips.twitch.tv/ExuberantEsteemedPistachioCurseLit-L-jTrUt1MRaZF1u3

This work in progress code is a rewrite and extension of an excellent system seen on DoudDougW's Twitch channel (https://www.twitch.tv/dougdougw). They've kindly provided the code on their website (https://www.dougdoug.com/twitchplays)

The inspiration and request was from my friend Kat who wants to use a similar concept to control Phasmophobia on her channel (https://www.twitch.tv/katatouille93)

I was unable to find the work on github, so created a fresh repository.  If anyone knows otherwise, please let me know so I can attribute this repo to their work in the usual Github way.

The initial commit on `main` (and now permanently on `archive`) shows the original files as taken from the website when I started this.  The original header is at the bottom of this Readme.  I've added a **GNU GPL v2** as I believe this license matches the header comments and way the code has been distributed before me.  Any issues, please do let me know.  Out of respect for all the contributors to this software and its inspiration, please do adhere to this license.  It is, I think, the most simple to understand and adhere to licence.

# Windows Defender
In the releases section of this repository are `exe` files you can download and try.  If you do download this `exe`, Windows Defender will throw a fit.  Feel free to Google "pyinstaller windows defender" to see what the issue is with needing to pay Microsoft for a certificate to prevent Defender going mad.  I can't justify the cost of a certificate, nor do I think it provides and security value, only convenience, which goes against the whole point of a security guarantee imo.

So you have a few options:
- Disable Windows Defender; Hell no.  Don't do this.  Anyone who tells you to is either an idiot, dangerous or both.
- Go into Windows Defender, look at the history, and allow this, and only this, `exe` that it has blocked.
- or, don't use the `exe`; instead run the raw Python (see below)

This code opens connections over the internet, sends and receives data and initiates HID (keyboard and mouse) commands.  It looks exactly like many Trojans.  It is only you, the human, that can decide whether it is malicious or not.  Hopefully you can see all the information here to inform that decision.  To assiste I have added Github actions which will show a green tech on the repository if it has passed code analysis scans for security.  These scans also happen weekly, so if a vulnerability exists that currently is not known about, becomes known, then that green tick will change to a red cross.  Hopefully, this provides peace of mind even if this software stops being maintained; you can still see whether it is still safe or not.

## Running the raw Python
Many tutorials on the internet on how to get Python.  I am using v3.10 and at least this version will be required.  There is a `requirements.txt` to make the process of getting dependencies easier, feel free to Google how to use this file with `pip` (one option is `pip install -r requirements.txt`).  One of the dependencies relies upon Windows.  Cross platform (MacOS, Linux, etc.) will not work, but if it is something you want, use the "issues" tab to create a feature request and I will take a look.

The only difference between running the `exe` or running the Python, is that the `exe` does not require the host machine to have Python installed, but does require an exception in Windows Defender.  I assume most broadcasters don't use Python, don't care about it and don't want to install loads of extra stuff on their machines.  The `exe` is also more portable as it doesn't care if you do already have Python installed, but the wrong version, missing dependencies, etc.

## Building your own exe
There is a batch script, `create_exe.bat` which you can run from a cmd window to build the `exe`.  This is what I use and I have included it in the repo for visibility for those concerned about the above security issues.

You will see that in the batch script there is a link to a `png` image to use as the `exe` icon.  This is image file is NOT included in this repo as I do not own the rights to distribute it as an image.  I am permitted by _katatouille93_ to use it embedded inside the `exe` for the icon.  You can just remove the `-i <image_file>` from the script, or change `<filename>` to an image of your choosing, if you want to fork this repo and create your own `exe`.

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
