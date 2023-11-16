# SimonSays

[![CodeQL Vulnerabilities](https://github.com/howroyd/simonsays/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/howroyd/simonsays/actions/workflows/codeql-analysis.yml)\
[![Bandit Python Vulnerabilities](https://github.com/howroyd/simonsays/actions/workflows/bandit.yml/badge.svg)](https://github.com/howroyd/simonsays/actions/workflows/bandit.yml)\
[![Linting and Testing](https://github.com/howroyd/simonsays/actions/workflows/python-testing.yml/badge.svg)](https://github.com/howroyd/simonsays/actions/workflows/python-testing.yml)\
[![Build and Release](https://github.com/howroyd/simonsays/actions/workflows/python-publish.yml/badge.svg)](https://github.com/howroyd/simonsays/actions/workflows/python-publish.yml)

Taking inspiration from the many other "TwitchPlays" style programmes, including that featured by [DougDoug](#original-file-header-comments), this software has been specifically created to be an easy to use for those non programmers among the gaming community.

Out of the box, this uses a [connection](https://github.com/howroyd/twitchirc) to Twitch chat, in a receive-only mode, to capture messages typed by viewers.  Connections to multiple different chats simultaneously is possible for collaboration streams!

Trigger words must be at the start of a sentence typed in chat and ***do not*** need to be prepended by a `!` like many other bots.  However, you can reconfigure the trigger words however you like.

The beautiful artwork is courtesy of the wonderful **Szinie**.  Please do show appreciation over on her [Twitch channel](https://www.twitch.tv/szinie).

## How To Guide

For basic installation and usage in a video format, I have recorded the below on YouTube:

[![How to guide video](https://img.youtube.com/vi/tYnfSwJiYAY/default.jpg)](https://youtu.be/tYnfSwJiYAY)

The latest release can be found [here](https://github.com/howroyd/simonsays/releases/latest).

## Gameplay Examples

[Chat driving player around Phasmo map](https://clips.twitch.tv/LachrymoseBetterPlumagePoooound-QCVryh5okrpf5rHB)

[Chat drives player around Phasmo lobby, handsfree](https://www.twitch.tv/videos/1978662007)


## Compatibility

This software talks directly to the operating system *as if* it were a mouse or keyboard plugged into your machine.  It does not modify any game code nor any files on your computer.  It has been tested in Windows and Linux.

The main use case to date has been for Phasmophobia streamers to allow their chat to troll them during gameplay.  Therefore, all the preset actions are Phasmophobia focused at the moment, however, if you would like another game to be considered then please raise a feature request [issue](https://github.com/howroyd/simonsays/issues) and I will look into it!  (Or, if you want to try your hand at programming, feel free to fork or PR this repository!)

### Windows Defender

Windows Defender will likely throw a fit if you download the executable and run it.  This is purely because I have not paid Microsoft for an exemption in Windows Defender.

So you have a few options:

- Disable Windows Defender; Hell no.  Don't do this.  Anyone who tells you to is either an idiot, dangerous or both.
- Go into Windows Defender, look at the history, and allow this, and only this, `exe` that it has blocked.
- ... or, don't use the `exe`; instead run the raw Python (see below)

This code opens connections over the internet, sends and receives data and initiates HID (keyboard and mouse) commands.  It looks exactly like many Trojans which do this nefariously.  It is only you, the human, that can decide whether it is malicious or not.  Hopefully you can see all the information here to inform that decision.  To assist I have added GitHub actions which will show a green tick on the repository if it has passed code analysis scans for security using `CodeQL`.  These scans also happen weekly, so if a vulnerability exists that currently is not known about, becomes known, then that green tick will change to a red cross.  Hopefully, this provides peace of mind even if this software stops being maintained; you can still see whether it is still safe or not.  Furthermore, I do not manually build the executables any more, this is done autonomously by GitHub *only* if the code scans pass at the time of release.

## Contributing and Thanks

This software is provided free of charge under the licence found [here](./LICENSE).  It is kindly requested that if you enjoy using SimonSays then please do promote the links to this so more people can have fun.

It would be fun to extend this to be able to connect to other chat servers such as, YouTube, Kick, etc.  If you're interested in this then please let me know by raising an [issue](https://github.com/howroyd/simonsays/issues).

If you would like to contribute artwork, programming, testing or in any other way, then please do get in touch in any way convenient, preferably [here](https://github.com/howroyd/simonsays/discussions).

No financial reward is expected to use this software, but if it is something you wish to consider then you can either sponsor this project or send a one off donation under [Sponsor this project](https://github.com/howroyd/simonsays).

You can find me on Twitch as [DrGreenGiant](https://www.twitch.tv/drgreengiant) and on [YouTube](https://youtube.com/@SimonHowroyd?si=wsQ0XuGwGjaXB7HU) too.

## Installation

### As an Executable

The latest release can be found [here](https://github.com/howroyd/simonsays/releases/latest).

Other releases are published on GitHub [here](https://github.com/howroyd/simonsays/releases).

Look for the one tagged in green `latest`.  At the bottom of that release you will see a drop-down box called **Assets** which has the `windows_release.zip` and `linux_release.tar.gz`.  Unzip the file to a location of your choice, e.g. your Desktop, and run the contained file.  It will generate a config file so that if you change any keybinding, etc, they will be remembered.

### As a Python Module

Available on PyPi at <https://pypi.org/project/simonsays-drgreengiant/>

```bash
pip install simonsays_drgreengiant
```

## Python Module Usage

If you install this as a Python module, then you can run the software by:

```python
from simonsays_drgreengiant import simonsays

simonsays.main()
```

## Original file header comments

Although this software is a complete re-write of the code that inspired me, I would still love to give credit to the original source code that got me started:

>
> Written by [DougDoug](https://www.twitch.tv/dougdoug) and DDarknut
>
> Hello! This file contains the main logic to process Twitch chat and convert it to game commands.
> The code is written in Python 3.X
> There are 2 other files needed to run this code:
>
> - `TwitchPlays_KeyCodes.py` contains the key codes and functions to press keys in-game. You should not modify this file.
> - `TwitchPlays_Connection.py` is the code that actually connects to Twitch. You should not modify this file.
>
> The source code primarily comes from:
>
> - Wituz's "Twitch Plays" tutorial: <http://www.wituz.com/make-your-own-twitch-plays-stream.html>
> - PythonProgramming's "Python Plays GTA V" tutorial: <https://pythonprogramming.net/direct-input-game-python-plays-gta-v/>
> - DDarknut's message queue and updates to the Twitch networking code
>
> Disclaimer:
>
> - This code is NOT intended to be professionally optimized or organized.
> - We created a simple version that works well for livestreaming, and I'm sharing it for educational purposes.
