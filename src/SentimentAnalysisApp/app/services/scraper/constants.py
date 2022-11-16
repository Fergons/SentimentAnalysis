from typing import Literal, Union, List, Optional
from datetime import datetime
from enum import Enum
from app.schemas import Source
from pydantic import BaseModel, validator, Field


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
            "user_reviews_url": "https://store.steampowered.com/appreviews/",
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
            "game_detail_url": "http://www.gamespot.com/api/games/",
            "list_of_games_url": "http://www.gamespot.com/api/games/",
        }
}


class SteamApiLanguageCodes(str, Enum):
    ARABIC = "arabic"
    BULGARIAN = "bulgarian"
    SCHINESE = "schinese"
    TCHINESE = "tchinese"
    CZECH = "czech"
    DANISH = "danish"
    DUTCH = "dutch"
    ENGLISH = "english"
    FINNISH = "finnish"
    FRENCH = "french"
    GERMAN = "german"
    GREEK = "greek"
    HUNGARIAN = "hungarian"
    ITALIAN = "italian"
    JAPANESE = "japanese"
    KOREANA = "koreana"
    NORWEGIAN = "norwegian"
    POLISH = "polish"
    PORTUGUESE = "portuguese"
    BRAZILIAN = "brazilian"
    ROMANIAN = "romanian"
    RUSSIAN = "russian"
    SPANISH = "spanish"
    LATAM = "latam"
    SWEDISH = "swedish"
    THAI = "thai"
    TURKISH = "turkish"
    UKRAINIAN = "ukrainian"
    VIETNAMESE = "vietnamese"


class SteamWebApiLanguageCodes(str, Enum):
    ARABIC = "ar"
    BULGARIAN = "bg"
    SCHINESE = "zh-CN"
    TCHINESE = "zh-TW"
    CZECH = "cs"
    DANISH = "da"
    DUTCH = "nl"
    ENGLISH = "en"
    FINNISH = "fi"
    FRENCH = "fr"
    GERMAN = "de"
    GREEK = "el"
    HUNGARIAN = "hu"
    ITALIAN = "it"
    JAPANESE = "ja"
    KOREANA = "ko"
    NORWEGIAN = "no"
    POLISH = "pl"
    PORTUGUESE = "pt"
    BRAZILIAN = "pt-BR"
    ROMANIAN = "ro"
    RUSSIAN = "ru"
    SPANISH = "es"
    LATAM = "es-419"
    SWEDISH = "sv"
    THAI = "th"
    TURKISH = "tr"
    UKRAINIAN = "uk"
    VIETNAMESE = "vn"


class SteamReviewQuerySummary(BaseModel):
    __name__ = "query_summary"
    num_reviews: int
    review_score: Optional[int] = None
    review_score_desc: Optional[str] = None
    total_positive: Optional[int] = None
    total_negative: Optional[int] = None
    total_reviews: Optional[int] = None


class SteamReviewer(BaseModel):
    steamid: int = Field(alias="source_reviewer_id")
    num_games_owned: int
    num_reviews: int
    playtime_forever: Optional[int] = None
    playtime_last_two_weeks: Optional[int] = None
    playtime_at_review: Optional[int] = None
    last_played: Optional[int] = None


class SteamReview(BaseModel):
    recommendationid: str = Field(alias="source_review_id")
    author: SteamReviewer
    language: Union[SteamApiLanguageCodes, SteamWebApiLanguageCodes]
    review: str
    timestamp_created: int
    timestamp_updated: int
    voted_up: bool
    votes_up: int
    votes_funny: int
    weighted_vote_score: str
    comment_count: int
    steam_purchase: bool
    received_for_free: bool
    written_during_early_access: bool


    class Config:
        use_enum_values = True


class SteamAppReleaseDate(BaseModel):
    coming_soon: bool
    date: datetime

    @validator("date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d %b, %Y"
        )


class SteamMetacriticReview(BaseModel):
    score: int
    url: str


class SteamAppCategory(BaseModel):
    id: int
    description: str


class SteamAppDetail(BaseModel):
    type: Literal["game"]
    name: str
    steam_appid: int = Field(alias="source_app_id")
    supported_languages: Optional[str] = None
    header_image: Optional[str] = Field(alias="image_url", default=None)
    developers: Optional[list] = None
    publishers: Optional[list] = None
    metacritic: Optional[SteamMetacriticReview] = None
    categories: List[SteamAppCategory] = []
    genres: List[SteamAppCategory] = []
    release_date: SteamAppReleaseDate

    class Config:
        allow_population_by_field_name = True


class SteamAppReviewsResponse(BaseModel):
    success: int
    cursor: str = "*"
    reviews: List[SteamReview]
    query_summary: SteamReviewQuerySummary
    error: str = ""

    @validator("success", pre=True)
    def validate_status(cls, value):
        if value == 1:
            return value
        else:
            raise ValueError(f"status:{value} error:{cls.error}")


class SteamAppDetailResponse(BaseModel):
    success: bool
    data: SteamAppDetail
    error: str = ""

    @validator("success", pre=True)
    def validate_status(cls, value):
        if value:
            return value
        else:
            raise ValueError(f"status:{value} error:{cls.error}")


