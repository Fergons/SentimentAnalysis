from datetime import datetime
from typing import List, Union, TYPE_CHECKING
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, Field, validator

if TYPE_CHECKING:
    from .review import Review
    from .source import Source


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


class GameCreateWithSource(GameBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    source_id: Optional[int] = None
    source_game_id: Optional[str] = None


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None


class GameInDBBase(GameBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Game(GameInDBBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass

class GameCategoryBase(BaseModel):
    game_id: int
    category_id: int

class GameCategoryCreate(GameCategoryBase):
    game_id: int
    category_id: int

class GameCategoryUpdate(GameCategoryBase):
    game_id: int
    category_id: int