from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl
# from . import SourceInDBBase, ReviewerInDBBase, GameInDBBase, AspectInDBBase
# from . import SourceCreate, ReviewerCreate, GameCreate, AspectCreate
from . import SourceBase, ReviewerBase, GameBase, AspectBase


class ReviewBase(BaseModel):
    text: str
    language: str
    source_review_id: str
    source: SourceBase
    reviewer: ReviewerBase
    game: GameBase

    aspect_sum_polarity: Optional[str] = None
    aspects: Optional[List[AspectBase]] = None


class ReviewCreate(ReviewBase):
    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None
    playtime_at_review: Optional[int] = None
    created_at: datetime = datetime.now()


# Properties to receive via API on update
class ReviewUpdate(ReviewBase):
    text: Optional[str] = None
    language: Optional[str] = None

    source: Optional[SourceBase] = None
    game: Optional[GameBase] = None

    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None

    playtime_at_review: Optional[int] = None

    aspect_sum_polarity: Optional[str] = None
    aspects: Optional[List[AspectBase]] = None


class ReviewInDBBase(ReviewBase):
    id: str
    game_id: int
    source_id: int
    user_id: int
    processed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Review(ReviewInDBBase):
    pass


# Additional properties stored in DB
class ReviewInDB(ReviewInDBBase):
    pass