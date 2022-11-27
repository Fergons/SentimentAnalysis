from datetime import datetime
from typing import List, Union, TYPE_CHECKING
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl

if TYPE_CHECKING:
    from .review import Review
    from .source import Source


class ReviewerBase(BaseModel):
    name: Optional[str] = None
    source_reviewer_id: str


class ReviewerCreate(ReviewerBase):
    name: Optional[str] = None
    source_id: Optional[int] = None
    source_reviewer_id: str
    num_games_owned: Optional[int] = None
    num_reviews: Optional[int] = None
    playtime_at_review: Optional[int] = None

# Properties to receive via API on update
class ReviewerUpdate(ReviewerBase):
    num_reviews: Optional[int] = None
    source: Optional["Source"] = None
    reviews: Optional[List["Review"]] = None


class ReviewerInDBBase(ReviewerBase):
    id: int
    source_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Reviewer(ReviewerInDBBase):
    num_reviews: int

# Additional properties stored in DB
class ReviewerInDB(ReviewerInDBBase):
    pass
