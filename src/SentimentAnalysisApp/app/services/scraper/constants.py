from typing import Literal, Union, List, Optional, Dict
from datetime import datetime
from enum import Enum
from app.schemas import Source
from pydantic import BaseModel, validator, Field
from pydantic.schema import schema


class SourceName(str, Enum):
    STEAM = 'steam'
    METACRITIC = 'metacritic'
    GAMESPOT = 'gamespot'
    ALL = 'all'


class ContentType(str, Enum):
    alias = "content-type"
    TEXT = "text/html"
    JSON = "application/json"
    HTML = "text/html"
    XML = "application/xml"


# 200 calls per 5 mins
STEAM_API_RATE_LIMIT = {"max_rate": 200, "time_period": 60}
DEFAULT_RATE_LIMIT = {"max_rate": 1000, "time_period": 60}

SOURCES = {
    SourceName.STEAM:
        {
            "url": "https://store.steampowered.com/api",
            "name": SourceName.STEAM,
            "user_reviews_url": "https://store.steampowered.com/appreviews",
            "game_detail_url": "https://store.steampowered.com/api/appdetails",
            "list_of_games_url": "https://api.steampowered.com/ISteamApps/GetAppList/v2",
        },

    SourceName.METACRITIC:
        {
            "url": "https://metacritic.com",
            "name": SourceName.METACRITIC,
            "user_reviews_url": "https://metacritic.com",
            "game_detail_url": "https://metacritic.com",
            "list_of_games_url": "https://metacritic.com",
        },

    SourceName.GAMESPOT:
        {
            "url": "https://www.gamespot.com/api/",
            "name": SourceName.GAMESPOT,
            "user_reviews_url": "https://www.gamespot.com/api/reviews/",
            "critic_reviews_url": "https://www.gamespot.com/api/reviews/",
            "game_detail_url": "http://www.gamespot.com/api/games/",
            "list_of_games_url": "http://www.gamespot.com/api/games/",
        }
}


