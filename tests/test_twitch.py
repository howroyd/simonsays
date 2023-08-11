import pytest

import twitchirc

DEFAULT_CHANNEL = "drgreengiant"


def test_message_enum():
    enumstringsexpected = {
        "JOIN": twitchirc.TwitchMessageEnum.JOIN,
        "PART": twitchirc.TwitchMessageEnum.PART,
        "NOTICE": twitchirc.TwitchMessageEnum.NOTICE,
        "CLEARCHAT": twitchirc.TwitchMessageEnum.CLEARCHAT,
        "HOSTTARGET": twitchirc.TwitchMessageEnum.HOSTTARGET,
        "PRIVMSG": twitchirc.TwitchMessageEnum.PRIVMSG,
        "PING": twitchirc.TwitchMessageEnum.PING,
        "CAP": twitchirc.TwitchMessageEnum.CAP,
        "GLOBALUSERSTATE": twitchirc.TwitchMessageEnum.GLOBALUSERSTATE,
        "USERSTATE": twitchirc.TwitchMessageEnum.USERSTATE,
        "ROOMSTATE": twitchirc.TwitchMessageEnum.ROOMSTATE,
        "RECONNECT": twitchirc.TwitchMessageEnum.RECONNECT,
        "421": twitchirc.TwitchMessageEnum.NUMERIC,
        "001": twitchirc.TwitchMessageEnum.NUMERIC,
        "002": twitchirc.TwitchMessageEnum.NUMERIC,
        "003": twitchirc.TwitchMessageEnum.NUMERIC,
        "004": twitchirc.TwitchMessageEnum.NUMERIC,
        "353": twitchirc.TwitchMessageEnum.NUMERIC,
        "366": twitchirc.TwitchMessageEnum.NUMERIC,
        "372": twitchirc.TwitchMessageEnum.NUMERIC,
        "375": twitchirc.TwitchMessageEnum.NUMERIC,
        "376": twitchirc.TwitchMessageEnum.NUMERIC,
        "hodsaflkfj": None,
        "  JOIN  \r\n": twitchirc.TwitchMessageEnum.JOIN,
        "join": twitchirc.TwitchMessageEnum.JOIN,
    }
    for key, val in enumstringsexpected.items():
        ret = twitchirc.TwitchMessageEnum.match_message_type(key)
        assert val == ret, f"Failed to parse \"{key}\" into {val}: got {ret}"


def channel_connection(channel: str):
    with twitchirc.TwitchIrc(channel) as irc:
        assert irc.connected, "Thought we were connected but flag isnt set"


# def test_bad_channel_connection():
#     with pytest.raises(twitchirc.TwitchIrcConnectionError):
#         channel_connection("")


# def test_good_channel_connection():
#     channel_connection(DEFAULT_CHANNEL)
