from datetime import datetime
from typing import List, TYPE_CHECKING, Dict, Tuple
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl

if TYPE_CHECKING:
    from .review import Review


class AspectBase(BaseModel):
    review_id: int
    term: str
    category: str
    polarity: str
    opinion: str
    model_id: str


class AspectCreate(AspectBase):
    review_id: int
    term: str = ""
    category: Optional[str] = None
    polarity: str
    opinion: Optional[str] = None
    model_id: str


# Properties to receive via API on update
class AspectUpdate(AspectBase):
    review_id: Optional[int] = None
    term: Optional[str] = None
    category: Optional[str] = None
    polarity: Optional[str] = None
    opinion: Optional[str] = None
    model_id: Optional[str] = None


class AspectInDBBase(AspectBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Aspect(AspectInDBBase):
    pass


# Additional properties stored in DB
class AspectInDB(AspectInDBBase):
    model_id: str

class AspectTermCount(BaseModel):
    term: str
    count: int

class AspectTermPolarityGroups(BaseModel):
    positive: List[AspectTermCount] = []
    negative: List[AspectTermCount] = []
    neutral: List[AspectTermCount] = []


class AspectWordcloud(BaseModel):
    categories: Dict[str, AspectTermPolarityGroups] = {}