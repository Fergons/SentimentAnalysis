from datetime import datetime
from typing import List, Union, TYPE_CHECKING, Literal
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, Field, validator

if TYPE_CHECKING:
    from developer import Developer


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


class GameListQuerySummary(BaseModel):
    total: int
    processed: Optional[int] = None


aspectCategories = Literal["gameplay", "performance & bugs", "audio & visual", "price", "community", "other"]


class GameListItem(BaseModel):
    id: int
    name: str
    image_url: Optional[AnyHttpUrl] = None
    release_date: Optional[datetime] = None
    categories: List[Category] = None
    developers: List["Developer"] = None
    score: Optional[str] = None
    num_reviews: int
    most_mentioned_aspects: List[aspectCategories] = None
    best_aspects: List[aspectCategories] = None
    worst_aspects: List[aspectCategories] = None

    @validator('categories', 'developers', 'best_aspects', 'worst_aspects', 'most_mentioned_aspects', pre=True)
    def set_default_lists(cls, v):
        return v or []

    class Config:
        orm_mode = True


class GameListResponse(BaseModel):
    query_summary: Optional[GameListQuerySummary] = None
    games: List[GameListItem]
    cursor: Optional[str] = None


class GameListFilter(BaseModel):
    name: Optional[str] = None
    categories: Optional[List[str]] = None
    developers: Optional[List[str]] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    min_num_reviews: Optional[int] = None
    max_num_reviews: Optional[int] = None
    min_release_date: Optional[datetime] = None
    max_release_date: Optional[datetime] = None
    best_aspects: Optional[List[str]] = None
    worst_aspects: Optional[List[str]] = None



class GameListSort(BaseModel):
    name: Optional[Literal["asc", "desc"]] = None
    release_date: Optional[Literal["asc", "desc"]] = None
    score: Optional[Literal["asc", "desc"]] = None
    num_reviews: Optional[Literal["asc", "desc"]] = None
