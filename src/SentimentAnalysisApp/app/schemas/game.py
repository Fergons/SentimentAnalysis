from datetime import datetime
from typing import List, Union
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from . import Review, SourceBase, ReviewBase


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    name: str


class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class Category(CategoryInDBBase):
    pass


class GameBase(BaseModel):
    name: str


class GameCreate(GameBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    categories: Optional[List[CategoryBase]] = None


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    reviews: Optional[List[ReviewBase]] = None
    categories: Optional[List[CategoryBase]] = None
    sources: Optional[List[SourceBase]] = None


class GameInDBBase(GameBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class Game(GameInDBBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    reviews: Optional[List[ReviewBase]] = None
    categories: Optional[List[CategoryBase]] = None
    sources: Optional[List[SourceBase]] = None


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass
