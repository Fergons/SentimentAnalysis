from datetime import datetime
from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel, Field, validator


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

    class Config:
        allow_population_by_field_name = True


class SteamReview(BaseModel):
    recommendationid: str = Field(alias="source_review_id")
    author: SteamReviewer = Field(alias="reviewer")
    language: Union[SteamApiLanguageCodes, SteamWebApiLanguageCodes]
    review: str = Field(alias="text")
    timestamp_created: int = Field(alias="created_at")
    timestamp_updated: int
    voted_up: bool
    votes_up: int
    votes_funny: int
    weighted_vote_score: str = Field(alias="helpful_score")
    comment_count: int
    steam_purchase: bool
    received_for_free: bool
    written_during_early_access: bool

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class SteamMetacriticReview(BaseModel):
    score: int
    url: Optional[str] = None


class SteamAppCategory(BaseModel):
    id: int
    description: str


class SteamAppDetail(BaseModel):
    type: str = ""
    name: str = ""
    steam_appid: int = Field(alias="source_game_id")
    supported_languages: Optional[str] = None
    header_image: Optional[str] = Field(alias="image_url", default=None)
    developers: Optional[list] = None
    publishers: Optional[list] = None
    metacritic: Optional[SteamMetacriticReview] = None
    categories: List[SteamAppCategory] = []
    genres: List[SteamAppCategory] = []
    release_date: Optional[datetime]

    class Config:
        allow_population_by_field_name = True

    @validator("release_date", pre=True)
    def parse_date(cls, value):
        if value["coming_soon"]:
            return None
        return datetime.strptime(
            value["date"],
            "%d %b, %Y"
        )


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
            raise ValueError(f"Response status: {value}")


class SteamAppDetailResponse(BaseModel):
    success: bool
    data: Optional[SteamAppDetail] = None
    error: str = ""

    @validator("success", pre=True)
    def validate_status(cls, value):
        if value:
            return value
        else:
            raise ValueError(f"Response status: {value}")


class SteamApp(BaseModel):
    name: str
    appid: int


class SteamAppListResponse(BaseModel):
    apps: List[SteamApp]

    def __init__(self, **kwargs):
        kwargs["apps"] = kwargs["applist"]["apps"]
        super().__init__(**kwargs)