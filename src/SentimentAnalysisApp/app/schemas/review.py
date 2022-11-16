from datetime import datetime
from typing import List, TYPE_CHECKING, Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl
# from . import SourceInDBBase, ReviewerInDBBase, GameInDBBase, AspectInDBBase
# from . import SourceCreate, ReviewerCreate, GameCreate, AspectCreate

if TYPE_CHECKING:
    from .reviewer import Reviewer
    from .source import Source
    from .game import Game
    from .aspect import Aspect


class ReviewBase(BaseModel):
    text: str
    language: str
    source_review_id: str
    source: "Source"
    reviewer: "Reviewer"
    game: "Game"

    aspect_sum_polarity: Optional[str] = None
    aspects: Optional[List["Aspect"]] = None


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

    source: Optional["Source"] = None
    game: Optional["Game"] = None

    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None

    playtime_at_review: Optional[int] = None

    aspect_sum_polarity: Optional[str] = None
    aspects: Optional[List["Aspect"]] = None


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