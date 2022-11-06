import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class GameBase(BaseModel):
    id: str


class GameCreate(GameBase):
    steam_app_id: str


# Properties to receive via API on update
class GameUpdate(GameBase):
    name: Optional[str] = None
    image_url: Optional[AnyHttpUrl] = None
    metacritic_user_reviews_url: Optional[AnyHttpUrl] = None
    gamespot_review_url: Optional[AnyHttpUrl] = None
    gamespot_user_reviews_url: Optional[AnyHttpUrl] = None


class GameInDBBase(GameBase):
    id: Optional[str] = None
    metacritic_updated_at: Optional[datetime.datetime] = None
    gamespot_updated_at: Optional[datetime.datetime] = None
    steam_updated_at: Optional[datetime.datetime] = None
    info_updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Game(GameInDBBase):
    pass


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass
