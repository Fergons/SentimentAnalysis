from typing import Optional, List, Union, TYPE_CHECKING
from pydantic import BaseModel, AnyHttpUrl, Field, validator
from datetime import datetime


class ScrapedGame(BaseModel):
    type: str = "game"
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    source_id: Optional[int] = None
    source_game_id: Optional[str] = None
    categories: Optional[List[str]] = None
    developers: Optional[List[str]] = None
    publishers: Optional[List[str]] = None
    platforms: Optional[List[str]] = None

    @validator("categories", "developers", "publishers", "platforms", always=True)
    def set_default_lists(cls, v):
        return v or []


class ScrapedReviewer(BaseModel):
    name: Optional[str] = None
    source_id: Optional[int] = None
    source_reviewer_id: Optional[str] = None
    num_games_owned: Optional[int] = None
    num_reviews: Optional[int] = None


class ScrapedReview(BaseModel):
    text: str
    language: str = None
    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None
    voted_up: Optional[bool] = None
    playtime_at_review: Optional[int] = None
    created_at: datetime = datetime.now()

    source_id: int = None

    game_id: int = None
    game: ScrapedGame = None

    reviewer: ScrapedReviewer = None
    source_review_id: str = None


    @validator("reviewer", "game", always=True)
    def set_source_id(cls, v, values):
        if v:
            if values.get("source_id") is not None:
                v.source_id = values.get("source_id")
            elif v.source_id is not None:
                values["source_id"] = v.source_id
            else:
                raise ValueError("Either source_id or reviewer.source_id or game.source_id must be set")
        return v

    @validator("game_id", always=True)
    def check_game_id(cls, v, values):
        if v is None and values.get("game") is None:
            raise ValueError("Either game_id or game must be set")
        return v