from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from review import ReviewBase


class CategoryBase(BaseModel):
    id: int
    name: str


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    name: str


class GameBase(BaseModel):
    id: int
    name: str
    image_url: Optional[AnyHttpUrl]
    release_timestamp: datetime


class GameCreate(GameBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_timestamp: Optional[datetime] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    source_id: Optional[int] = None
    source_app_id: Optional[int] = None
    source_url: Optional[str] = None


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    release_timestamp: Optional[datetime] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    source_id: Optional[int] = None
    source_app_id: Optional[int] = None
    source_url: Optional[str] = None


class GameInDBBase(GameBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class Game(GameInDBBase):
    pass


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass
