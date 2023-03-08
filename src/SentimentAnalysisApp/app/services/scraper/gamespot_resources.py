import os
from datetime import datetime
from enum import Enum
from typing import Optional, Union, List, Any, Literal, Iterable, Tuple, TypeVar
from pydantic import BaseModel, Field, validator, AnyHttpUrl, root_validator

GAMESPOT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class GamespotGamesSortFields(str, Enum):
    _id = "id"
    name = "name"
    release_date = "release_date"


class GamespotReviewsSortFields(str, Enum):
    _id = "id"
    title = "title"
    publish_date = "publish_date"
    update_date = "update_date"
    score = "score"


class GamespotGamesFilterFields(str, Enum):
    _id = "id"
    name = "name"
    upc = "upc"
    association = "association"
    release_date = "release_date"


class GamespotReviewsFilterFields(str, Enum):
    _id = "id"
    title = "title"
    publish_date = "publish_date"
    update_date = "update_date"


class GamespotFilterParam(BaseModel):
    field: Union[GamespotGamesFilterFields, GamespotReviewsFilterFields]
    value: Union[str, int, datetime, Tuple[datetime, datetime]]

    @property
    def string(self):
        if isinstance(self.value, tuple):
            start = self.value[0].strftime(GAMESPOT_DATETIME_FORMAT)
            end = self.value[1].strftime(GAMESPOT_DATETIME_FORMAT)
            return f"{self.field}:{start}|{end}"

        if isinstance(self.value, datetime):
            start = self.value.strftime(GAMESPOT_DATETIME_FORMAT)
            end = datetime.now().strftime(GAMESPOT_DATETIME_FORMAT)
            return f"{self.field}:{start}|{end}"

        return f"{self.field}:{self.value}"

    class Config:
        use_enum_values = True


class GamespotSortParam(BaseModel):
    field: Union[GamespotGamesSortFields, GamespotReviewsSortFields]
    direction: SortDirection

    @property
    def string(self):
        return f"{self.field}:{self.direction}"

    class Config:
        use_enum_values = True


class GamespotImage(BaseModel):
    square_tiny: Optional[str] = None
    screen_tiny: Optional[str] = None
    square_small: Optional[str] = None
    original: Optional[str] = None


class GamespotGenre(BaseModel):
    name: str


class GamespotTheme(BaseModel):
    name: str


class GamespotFranchise(BaseModel):
    name: str


game_tags = {
    "Driving/Racing": "Racing",
    "Shooter": "FPS",
    "Role-Playing": "RPG",
}


class GamespotGame(BaseModel):
    id: int = Field(alias="source_game_id")
    name: str
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    deck: Optional[str] = None
    image: Optional[GamespotImage] = None
    categories: List[str] = []
    themes: Optional[List[GamespotTheme]] = []
    franchises: Optional[List[GamespotFranchise]] = None
    images_api_url: Optional[AnyHttpUrl] = None
    reviews_api_url: Optional[AnyHttpUrl] = None
    articles_api_url: Optional[AnyHttpUrl] = None
    videos_api_url: Optional[AnyHttpUrl] = None
    releases_api_url: Optional[AnyHttpUrl] = None
    site_detail_url: Optional[AnyHttpUrl] = None

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def create_categories(cls, values):
        categories = []
        for genre in values.get("genres", []):
            genre_name = genre.get("name")
            if genre_name is None:
                continue
            if genre_name in game_tags:
                categories.append(game_tags[genre_name])
            else:
                categories.append(genre_name)
        values["categories"] = categories
        return values

    @validator("release_date", pre=True)
    def parse_dates(cls, value):
        return datetime.strptime(
            value,
            GAMESPOT_DATETIME_FORMAT
        )


class GamespotReviewer(BaseModel):
    source_reviewer_id: str = Field(alias="source_reviewer_id", default="")
    name: str = ""

    class Config:
        allow_population_by_field_name = True


class GamespotReview(BaseModel):
    id: int = Field(alias="source_review_id")
    authors: GamespotReviewer = Field(alias="reviewer")
    lede: str = Field(alias="text")
    language: str = "english"
    publish_date: datetime = Field(alias="created_at")
    update_date: datetime
    review_type: str
    title: str
    image: GamespotImage
    score: str
    deck: str
    good: str
    bad: str
    game: Optional[GamespotGame] = None
    site_detail_url: str

    class Config:
        allow_population_by_field_name = True

    # @validator("good", "bad", pre=True)
    # def parse_good_bad(cls, value):
    #     if value == "":
    #         return []
    #     return value.split("|")

    @validator("publish_date", "update_date", pre=True)
    def parse_dates(cls, value):
        return datetime.strptime(
            value,
            GAMESPOT_DATETIME_FORMAT
        )


class GamespotRequestParams(BaseModel):
    api_key: str = os.environ.get("GAMESPOT_API_KEY")
    format: Literal["xml", "json", "jsonp"] = "json"
    field_list: Optional[str] = None
    limit: int = 100
    offset: int = 0
    sort: Optional[GamespotSortParam] = None  # &sort=field:direction where direction is either asc or desc.
    # Single filter: &filter=field:value | Multiple filters: &filter=field:value,field:value
    # Date filters: &filter=field:start date|end date (using datetime format)
    # Associations: &association=guid
    filter: Optional[List[GamespotFilterParam]] = None

    @validator("field_list", always=True, pre=True)
    def create_field_list(cls, value) -> Optional[str]:
        if isinstance(value, list):
            return ",".join(value)
        else:
            return value

    @validator("sort")
    def validate_sort(cls, value):
        if value is not None:
            return value.string

    @validator("filter")
    def validate_filter(cls, value):
        if value is not None:
            return ",".join([v.string for v in value]),

    class Config:
        json_encoders = {
            "sort": lambda v: v.string,
            "filter": lambda vs: ",".join([v.string for v in vs]),
            "field_list": lambda vs: ",".join(vs)
        }


class GamespotApiResponse(BaseModel):
    status_code: int
    error: str
    number_of_total_results: int
    number_of_page_results: int
    limit: int = 100
    offset: int = 0
    results: List[Union[GamespotGame, GamespotReview]]
    version: str

    @validator("status_code")
    def check_status(cls, value, values):
        if value == 1:
            return value
        raise ValueError(f"Api call unsuccessful: {values['error']}")
