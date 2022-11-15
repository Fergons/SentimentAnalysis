from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from . import Review, Reviewer, Game


class SourceBase(BaseModel):
    name: str
    url: AnyHttpUrl
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None
    list_of_games_url: Optional[AnyHttpUrl] = None
    reviews: Optional[List[Review]] = None
    reviewers: Optional[List[Reviewer]] = None
    games: Optional[List[Game]] = None


class SourceCreate(SourceBase):
    name: str
    url: AnyHttpUrl
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None
    list_of_games_url: Optional[AnyHttpUrl] = None
    reviews: Optional[List[Review]] = None
    reviewers: Optional[List[Reviewer]] = None
    games: Optional[List[Game]] = None


class SourceUpdate(SourceBase):
    name: Optional[str] = None
    url: Optional[AnyHttpUrl] = None
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None
    list_of_games_url: Optional[AnyHttpUrl] = None
    reviews: Optional[List[Review]] = None
    reviewers: Optional[List[Reviewer]] = None
    games: Optional[List[Game]] = None


class SourceInDBBase(SourceBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class Source(SourceInDBBase):
    pass
