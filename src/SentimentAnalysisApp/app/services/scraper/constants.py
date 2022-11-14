from enum import Enum


class Source:
    STEAM = 'steam'
    METACRITIC = 'metacritic'
    GAMESPOT = 'gamespot'
    ALL='all'


class ContentType:
    TEXT = "text"
    JSON = "json"
    HTML = "html"
    XML = "xml"


# 200 calls per 5 mins
STEAM_API_RATE_LIMITS = {"max_rate": 200, "time_period": 60}