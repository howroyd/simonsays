import contextlib
import threading
import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from . import config

TITLE = "Simon Says API"

SUMMARY = "A FastAPI interface to the Simon Says app runtime"

DESCRIPTION = """## General

Intended for developers, this API provides access to Simon Says to set and query runtime behaviour.

This API is not intended for use by end users, but go for it if you want!

## Developer Information

Created by Simon Howroyd (DrGreenGiant), 2024.  [GitHub](https://github.com/howroyd/simonsays)
"""

CONTACT = {"name": "DrGreenGiant", "url": "https://github.com/howroyd/simonsays"}


def root():
    return RedirectResponse(url="/docs")


def make_commands(myconfig: config.Config) -> str:
    def commands() -> str:
        return f"Valid commands are:\n{config.make_commands_str(myconfig)}"

    return commands


def make_bot_list(myconfig: config.Config) -> str:
    def bot_list():
        return myconfig.bots

    return bot_list


def make_config(myconfig: config.Config):
    def config_viewer() -> dict:
        return {k: {"twitch": v.twitch, "hid": v.phasmo.hidconfig} for k, v in myconfig.config.items()}

    return config_viewer


def make_twitch_channels(myconfig: config.Config):
    def twitch_channels_viewer() -> set:
        return myconfig.channel

    return twitch_channels_viewer


def twitch_channel():
    return RedirectResponse(url="/channels")


def make_command_setter(myconfig: config.Config):
    def command_setter(command: str, value: bool) -> str:
        if command not in myconfig.config:
            return f"Invalid command {command}.  {make_commands(myconfig)()}"
        myconfig.config[command].twitch.enabled = value
        return f"Set {command} enabled to {value}"

    return command_setter


def make_api(myconfig: config.Config) -> FastAPI:
    ret = FastAPI(title=TITLE, summary=SUMMARY, description=DESCRIPTION, version=myconfig.version, contact=CONTACT)

    ret.add_api_route("/", endpoint=root)
    ret.add_api_route("/commands", endpoint=make_commands(myconfig))
    ret.add_api_route("/config", endpoint=make_config(myconfig))
    ret.add_api_route("/bots", endpoint=make_bot_list(myconfig))
    ret.add_api_route("/channels", endpoint=make_twitch_channels(myconfig))
    ret.add_api_route("/channel", endpoint=twitch_channel)

    ret.add_api_route("/channel", endpoint=make_command_setter(myconfig), methods=["POST"])

    return ret


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self) -> None:
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(0.1)
            yield
        finally:
            self.should_exit = True
            thread.join()


def make_server(myconfig: config.Config):
    def app_fn() -> FastAPI:
        return make_api(myconfig)

    apiconfig = uvicorn.Config(app=app_fn, factory=True, host="127.0.0.1", port=8000)
    apiserver = Server(config=apiconfig)

    return apiserver.run_in_thread
