from datetime import datetime
from typing import List, TYPE_CHECKING
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl

if TYPE_CHECKING:
    from .review import Review


class AspectBase(BaseModel):
    term: str
    category: str
    polarity: str
    confidence: str
    review: "Review"


class AspectCreate(AspectBase):
    confidence: Optional[str] = None


# Properties to receive via API on update
class AspectUpdate(AspectBase):
    term: Optional[str] = None
    category: Optional[str] = None
    polarity: Optional[str] = None
    confidence: Optional[str] = None


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
