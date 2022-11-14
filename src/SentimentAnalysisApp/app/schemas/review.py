import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl


class ReviewBase(BaseModel):
    text: str
    source_url: AnyHttpUrl


class ReviewCreate(ReviewBase):
    text: str
    source_review_id: Optional[str] = None
    source_id: Optional[int] = None
    source_url: Optional[AnyHttpUrl] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None
    reviewer_id: Optional[str] = None
    reviewer_time_played_at_review: Optional[int] = None
    game_id: Optional[str] = None
    game_name: Optional[str] = None


# Properties to receive via API on update
class ReviewUpdate(ReviewBase):
    text: Optional[str] = None
    source_id: Optional[int] = None
    source_url: Optional[AnyHttpUrl] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None
    reviewer_id: Optional[str] = None
    reviewer_time_played_at_review: Optional[int] = None
    game_id: Optional[str] = None
    game_name: Optional[str] = None


class ReviewInDBBase(ReviewBase):
    id: str
    game_id: int
    user_id: int
    processed_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Review(ReviewInDBBase):
    pass


# Additional properties stored in DB
class ReviewInDB(ReviewInDBBase):
    pass