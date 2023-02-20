from datetime import datetime
from typing import List, TYPE_CHECKING, Optional, Union, Literal
from pydantic import BaseModel, EmailStr, AnyHttpUrl
# from . import SourceInDBBase, ReviewerInDBBase, GameInDBBase, AspectInDBBase
# from . import SourceCreate, ReviewerCreate, GameCreate, AspectCreate

if TYPE_CHECKING:
    from .reviewer import ReviewerCreate
    from .source import Source
    from .game import Game, GameCreate
    from .aspect import Aspect

TimeInterval = Literal["day", "week", "month", "year"]

class ReviewBase(BaseModel):
    text: str
    language: str


class ReviewCreate(ReviewBase):
    text: str
    language: str = None
    reviewer_id: int = None
    game_id: int = None
    source_id: int = None
    source_review_id: str = None
    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None
    voted_up: Optional[bool] = None
    playtime_at_review: Optional[int] = None
    created_at: datetime = datetime.now()


# Properties to receive via API on update
class ReviewUpdate(ReviewBase):
    text: Optional[str] = None
    language: Optional[str] = None

    source_id: Optional[int] = None
    game_id: Optional[int] = None

    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None

    playtime_at_review: Optional[int] = None

    aspect_sum_polarity: Optional[str] = None


class ReviewInDBBase(ReviewBase):
    id: int
    game_id: Optional[int] = None
    source_id: Optional[int] = None
    user_id: Optional[int] = None
    processed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    source_review_id: Union[int, str, None] = None

    class Config:
        orm_mode = True


class Review(ReviewInDBBase):
    pass


class ReviewWithAspects(ReviewInDBBase):
    aspects: List["Aspect"] = []


class ReviewsSummary(BaseModel):
    total: int
    num_reviews: int = 0
    processed: List[int] = []
    not_processed: List[int] = []
    source_id: Optional[int] = None
    game_id: Optional[int] = None
    positive: List[int] = []
    negative: List[int] = []
    neutral: List[int] = []

# Additional properties stored in DB
class ReviewInDB(ReviewInDBBase):
    pass