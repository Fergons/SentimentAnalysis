import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl


class ReviewerBase(BaseModel):
    source_id: int


class ReviewerCreate(ReviewerBase):
    source_id: Optional[int] = None
    source_url: AnyHttpUrl
    num_reviews: Optional[int] = None


# Properties to receive via API on update
class ReviewerUpdate(ReviewerBase):
    source_id: Optional[int] = None
    source_url: Optional[AnyHttpUrl] = None
    num_reviews: Optional[int] = None


class ReviewerInDBBase(ReviewerBase):
    id: int
    source_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Reviewer(ReviewerInDBBase):
    pass


# Additional properties stored in DB
class ReviewerInDB(ReviewerInDBBase):
    pass
