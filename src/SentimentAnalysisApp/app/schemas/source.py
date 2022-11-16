from datetime import datetime
from typing import List, TYPE_CHECKING, Union
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from . import Review, Reviewer, Game

if TYPE_CHECKING:
    from .reviewer import Reviewer
    from .review import Review
    from .game import Game


class SourceBase(BaseModel):
    name: str
    url: Optional[AnyHttpUrl] = None
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None
    game_detail_url: Optional[AnyHttpUrl] = None
    list_of_games_url: Optional[AnyHttpUrl] = None
    reviewer_detail_url: Optional[AnyHttpUrl] = None
    list_of_reviewers_url: Optional[AnyHttpUrl] = None

class SourceCreate(SourceBase):
    name: str
    url: AnyHttpUrl
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None
    game_detail_url: Optional[AnyHttpUrl] = None
    list_of_games_url: Optional[AnyHttpUrl] = None
    reviewer_detail_url: Optional[AnyHttpUrl] = None
    list_of_reviewers_url: Optional[AnyHttpUrl] = None


class SourceUpdate(SourceBase):
    name: Optional[str] = None
    url:  Optional[AnyHttpUrl] = None
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None
    game_detail_url: Optional[AnyHttpUrl] = None
    list_of_games_url: Optional[AnyHttpUrl] = None
    reviewer_detail_url: Optional[AnyHttpUrl] = None
    list_of_reviewers_url: Optional[AnyHttpUrl] = None
    reviews: Optional[List["Review"]] = None
    reviewers: Optional[List["Reviewer"]] = None
    games: Optional[List["Game"]] = None


class SourceInDBBase(SourceBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class Source(SourceInDBBase):
    reviews: Optional[List["Review"]] = None
    reviewers: Optional[List["Reviewer"]] = None
    games: Optional[List["Game"]] = None
