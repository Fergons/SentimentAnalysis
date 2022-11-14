from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from .review import ReviewBase


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    name: str


class GameBase(BaseModel):
    name: str
    image_url: Optional[AnyHttpUrl]
    release_date: datetime


class GameCreate(GameBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    categories_ids: Optional[List[int]] = None
    categories_names: Optional[List[str]] = None
    source_id: Optional[int] = None
    source_app_id: Optional[int] = None
    source_url: Optional[str] = None


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    categories_ids: Optional[List[int]] = None
    categories_names: Optional[List[str]] = None
    source_id: Optional[int] = None
    source_app_id: Optional[int] = None
    source_url: Optional[str] = None


class GameInDBBase(GameBase):
    id: int
    class Config:
        orm_mode = True


# Additional properties to return via API
class Game(GameInDBBase):
    pass


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass
