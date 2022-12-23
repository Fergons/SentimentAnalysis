from datetime import datetime
from typing import List, Union, TYPE_CHECKING
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, Field

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
    source_id: Optional[int] = None
    source_game_id: str
    # categories: Optional[List["CategoryCreate"]] = None


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    reviews: Optional[List["Review"]] = None
    categories: Optional[List[CategoryBase]] = None


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
