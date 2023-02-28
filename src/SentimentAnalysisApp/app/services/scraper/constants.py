from enum import Enum

class ScrapingResourceType(str, Enum):
    alias = "scraping-type"
    GAME = "game"
    REVIEW = "review"
    REVIEWER = "reviewer"
    SOURCE = "source"

class SourceName(str, Enum):
    STEAM = 'steam'
    METACRITIC = 'metacritic'
    GAMESPOT = 'gamespot'
    DOUPE = 'doupe'
    ALL = 'all'


class ContentType(str, Enum):
    alias = "content-type"
    TEXT = "text/html"
    JSON = "application/json"
    HTML = "text/html"
    XML = "application/xml"


# 200 calls per 5 mins
STEAM_API_RATE_LIMIT = {"max_rate": 200, "time_period": 300}
STEAM_REVIEWS_API_RATE_LIMIT = {"max_rate": 200, "time_period": 300}
DEFAULT_RATE_LIMIT = {"max_rate": 10, "time_period": 4}

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
        },

    SourceName.DOUPE:
        {
            "url": "https://doupe.zive.cz",
            "name": SourceName.DOUPE,
            "user_reviews_url": "https://doupe.zive.cz/recenze/",
            "critic_reviews_url": "https://doupe.zive.cz/recenze/",
            "game_detail_url": None,
            "list_of_games_url": None,
        },
}


