import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: str


class UserCreate(UserBase):
    id: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    num_reviews: Optional[int] = None
    num_games_owned: Optional[int] = None


class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass
