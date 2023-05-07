"""
Created by Frantisek Sabol
This file contains constants used by the scrapers.
"""
from enum import Enum
from typing import Optional, List, Literal, Union

from pydantic import BaseModel, validator, root_validator


class ScrapingMode(str, Enum):
    alias = "scraping-mode"
    REVIEWS_OF_GAME = "reviews_of_game"
    REVIEWS_FROM_REVIEWER = "reviews_from_reviewer"
    REVIEWS_FROM_SOURCE = "reviews_from_source"
    REVIEWERS_OF_GAME = "reviewers_of_game"
    REVIEWERS_FROM_SOURCE = "reviewers_from_source"
    REVIEWS_OF_GAME_FROM_SOURCE = "reviews_of_game_from_source"
    REVIEWS_OF_GAME_FROM_REVIEWER = "reviews_of_game_from_reviewer"
    REVIEWERS_OF_GAME_FROM_SOURCE = "reviewers_of_game_from_source"
    GAMES_FROM_SOURCE = "games_from_source"


class ScrapingResource(str, Enum):
    alias = "scraping-resource"
    REVIEW = "review"
    REVIEWER = "reviewer"
    GAME = "game"
    GAME_CATEGORY = "game_category"
    GAME_PLATFORM = "game_platform"
    GAME_DEVELOPER = "game_developer"


class ScrapingBaseCriteria(BaseModel):
    game_id: Optional[int] = None
    reviewer_id: Optional[int] = None
    source_id: Optional[int] = None
    limit: Optional[int] = None


class ScrapingReviewsFilter(ScrapingBaseCriteria):
    language: Optional[str] = "czech"
    day_range: Optional[int] = None
    polarity: Optional[Literal["positive", "negative", "neutral"]] = None


class ScrapingReviewersFilter(ScrapingBaseCriteria):
    pass


class ScrapingGamesFilter(ScrapingBaseCriteria):
    pass


class ScraperTask(BaseModel):
    scraping_mode: ScrapingMode
    scraping_resources: List[ScrapingResource]
    scraping_criteria: Optional[ScrapingBaseCriteria] = None

    @validator("scraping_mode", pre=True, always=True)
    def validate_scraping_mode(cls, value, values):
        """
        Validate that scraping_mode is not None and that it is an element of the enum ScrapingMode.
        Validate that scraping_resources contains targets expected by the scraping_mode
        if scraping_resources is None set it to ScrapingResource list based on scraping_mode.
        """
        if values["scraping_resources"] is not None:
            return values

        _type = type(value)
        if _type is not ScrapingMode or _type is not str:
            raise ValueError(f"scraping_mode can only be of type {ScrapingMode} or str, not {_type}")
        if _type is str:
            value = ScrapingMode(value)

        if value == ScrapingMode.REVIEWS_FROM_REVIEWER:
            values["scraping_resources"] = [ScrapingResource.REVIEW, ScrapingResource.GAME]
        elif value == ScrapingMode.REVIEWS_OF_GAME:
            values["scraping_resources"] = [ScrapingResource.REVIEW, ScrapingResource.REVIEWER]
        elif value == ScrapingMode.REVIEWS_FROM_SOURCE:
            values["scraping_resources"] = [ScrapingResource.REVIEW, ScrapingResource.GAME, ScrapingResource.REVIEWER]
        elif value == ScrapingMode.REVIEWERS_OF_GAME:
            values["scraping_resources"] = [ScrapingResource.REVIEWER]
        elif value == ScrapingMode.REVIEWERS_FROM_SOURCE:
            values["scraping_resources"] = [ScrapingResource.REVIEWER]
        elif value == ScrapingMode.REVIEWS_OF_GAME_FROM_SOURCE:
            values["scraping_resources"] = [ScrapingResource.REVIEW, ScrapingResource.REVIEWER]
        elif value == ScrapingMode.REVIEWS_OF_GAME_FROM_REVIEWER:
            values["scraping_resources"] = [ScrapingResource.REVIEW]
        elif value == ScrapingMode.REVIEWERS_OF_GAME_FROM_SOURCE:
            values["scraping_resources"] = [ScrapingResource.REVIEWER]
        elif value == ScrapingMode.GAMES_FROM_SOURCE:
            values["scraping_resources"] = [ScrapingResource.GAME]
        else:
            raise ValueError("scraping_mode is not valid")
        return values


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
DEFAULT_RATE_LIMIT = {"max_rate": 10, "time_period": 3}
STEAM_API_RATE_LIMIT = {"max_rate": 2, "time_period": 4}
STEAM_REVIEWS_API_RATE_LIMIT = DEFAULT_RATE_LIMIT

SOURCES = {
    SourceName.STEAM.value:
        {
            "url": "https://store.steampowered.com/api",
            "name": SourceName.STEAM,
            "rate_limit": DEFAULT_RATE_LIMIT,
            "endpoints": {
                "user_reviews": {
                    "url": "https://store.steampowered.com/appreviews",
                    "content_type": ContentType.JSON.value,
                    "scraping_resources": [ScrapingResource.REVIEW.value, ScrapingResource.REVIEWER.value],
                    "scraping_mode": ScrapingMode.REVIEWS_OF_GAME_FROM_SOURCE.value
                },
                "game_detail": {
                    "url": "https://store.steampowered.com/api/appdetails",
                    "content_type": ContentType.JSON.value,
                    "rate_limit": STEAM_API_RATE_LIMIT,
                    "scraping_resources": [ScrapingResource.GAME.value],
                    "scraping_mode": ScrapingMode.GAMES_FROM_SOURCE.value
                },
                "list_of_games": {
                    "url": "https://api.steampowered.com/ISteamApps/GetAppList/v2",
                    "content_type": ContentType.JSON.value,
                    "scraping_resources": [ScrapingResource.GAME.value],
                    "scraping_mode": ScrapingMode.GAMES_FROM_SOURCE.value
                }
            },
            "user_reviews_url": "https://store.steampowered.com/appreviews",
            "game_detail_url": "https://store.steampowered.com/api/appdetails",
            "list_of_games_url": "https://api.steampowered.com/ISteamApps/GetAppList/v2"
        },

    SourceName.METACRITIC.value:
        {
            "url": "https://metacritic.com",
            "name": SourceName.METACRITIC,
            "user_reviews_url": "https://metacritic.com",
            "game_detail_url": "https://metacritic.com",
            "list_of_games_url": "https://metacritic.com",
            "rate_limit": DEFAULT_RATE_LIMIT
        },

    SourceName.GAMESPOT.value:
        {
            "url": "https://www.gamespot.com/api/",
            "name": SourceName.GAMESPOT,
            "user_reviews_url": "https://www.gamespot.com/api/reviews/",
            "critic_reviews_url": "https://www.gamespot.com/api/reviews/",
            "game_detail_url": "http://www.gamespot.com/api/games/",
            "list_of_games_url": "http://www.gamespot.com/api/games/",
            "rate_limit": DEFAULT_RATE_LIMIT,
            "endpoints": {
                "critic_reviews": {
                    "url": "https://www.gamespot.com/api/reviews/",
                    "content_type": ContentType.JSON.value,
                    "scraping_resources": [ScrapingResource.REVIEW.value],
                    "scraping_mode": ScrapingMode.REVIEWS_OF_GAME_FROM_SOURCE.value
                }
            }
        },

    SourceName.DOUPE.value:
        {
            "url": "https://doupe.zive.cz",
            "name": SourceName.DOUPE,
            "user_reviews_url": "https://doupe.zive.cz/recenze/",
            "critic_reviews_url": "https://doupe.zive.cz/recenze/",
            "game_detail_url": None,
            "list_of_games_url": None,
            "rate_limit": DEFAULT_RATE_LIMIT,
            "endpoints": {
                "critic_reviews": {
                    "url": "https://doupe.zive.cz/recenze/",
                    "content_type": ContentType.HTML.value,
                    "scraping_resources": [ScrapingResource.REVIEW.value],
                    "scraping_mode": ScrapingMode.REVIEWS_FROM_SOURCE.value
                }
            }
        }
}
