import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl


class ReviewBase(BaseModel):
    review: str
    created_at: datetime.datetime
    source_url: AnyHttpUrl


class ReviewCreate(ReviewBase):
    game_id: str
    user_id: int


# Properties to receive via API on update
class ReviewUpdate(ReviewBase):
    language: Optional[str] = None
    review: Optional[str] = None
    summary: Optional[str] = None
    score: Optional[str] = None
    helpful_score: Optional[str] = None
    good: Optional[str] = None
    bad: Optional[str] = None
    apect_sum_polarity: Optional[str] = None


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