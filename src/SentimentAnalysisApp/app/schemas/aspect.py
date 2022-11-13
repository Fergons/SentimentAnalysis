import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class AspectBase(BaseModel):
    id: id
    term: str
    category: str
    polarity: str
    confidence: str
    review_id: int


class AspectCreate(AspectBase):
    term: str
    category: str
    polarity: str
    confidence: Optional[str] = None
    review_id: Optional[int] = None


# Properties to receive via API on update
class AspectUpdate(AspectBase):
    term: Optional[str] = None
    category: Optional[str] = None
    polarity: Optional[str] = None
    confidence: Optional[str] = None
    review_id: Optional[int] = None


class AspectInDBBase(AspectBase):
    id: Optional[str] = None
    metacritic_updated_at: Optional[datetime.datetime] = None
    Aspectspot_updated_at: Optional[datetime.datetime] = None
    steam_updated_at: Optional[datetime.datetime] = None
    info_updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Aspect(AspectInDBBase):
    pass


# Additional properties stored in DB
class AspectInDB(AspectInDBBase):
    pass