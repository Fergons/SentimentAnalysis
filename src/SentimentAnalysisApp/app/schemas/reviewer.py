import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr


class ReviewerBase(BaseModel):
    id: int

class ReviewerCreate(ReviewerBase):
    id: str


# Properties to receive via API on update
class ReviewerUpdate(ReviewerBase):
    num_reviews: Optional[int] = None
    num_games_owned: Optional[int] = None


class ReviewerInDBBase(ReviewerBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Reviewer(ReviewerInDBBase):
    pass


# Additional properties stored in DB
class ReviewerInDB(ReviewerInDBBase):
    pass
