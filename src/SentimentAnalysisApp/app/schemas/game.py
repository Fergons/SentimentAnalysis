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


class GameFromSourceCreate(GameCreate):
    source_id: int
    source_game_id: str


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    reviews: Optional[List["Review"]] = None
    categories: Optional[List[CategoryBase]] = None


class GameFromSourceUpdate(GameUpdate):
    source_id: int
    source_game_id: str


class GameInDBBase(GameBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class Game(GameInDBBase):
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    reviews: Optional[List["Review"]] = None
    categories: Optional[List[CategoryBase]] = None
    sources: Optional[List[GameFromSourceCreate]] = None


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass
