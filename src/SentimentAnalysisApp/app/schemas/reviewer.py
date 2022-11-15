import datetime
from typing import List, Union
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl
from . import ReviewBase, SourceBase


class ReviewerBase(BaseModel):
    name: str
    source_reviewer_id: str
    source: SourceBase


class ReviewerCreate(ReviewerBase):
    name: str
    source_reviewer_id: str
    source: SourceBase
    num_reviews: Optional[int] = None
    reviews: Optional[List[ReviewBase]] = None


# Properties to receive via API on update
class ReviewerUpdate(ReviewerBase):
    num_reviews: Optional[int] = None
    source: Optional[SourceBase]
    reviews: Optional[List[ReviewBase]] = None


class ReviewerInDBBase(ReviewerBase):
    id: int
    source_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Reviewer(ReviewerInDBBase):
    num_reviews: int
    reviews: List[ReviewBase] = []

# Additional properties stored in DB
class ReviewerInDB(ReviewerInDBBase):
    pass
