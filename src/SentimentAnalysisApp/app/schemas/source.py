from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from review import ReviewBase


class SourceBase(BaseModel):
    id: int
    url: AnyHttpUrl
    user_reviews_url: Optional[AnyHttpUrl]
    critic_reviews_url: Optional[AnyHttpUrl]


class SourceCreate(SourceBase):
    url: AnyHttpUrl
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None


class SourceUpdate(SourceBase):
    url: Optional[AnyHttpUrl] = None
    user_reviews_url: Optional[AnyHttpUrl] = None
    critic_reviews_url: Optional[AnyHttpUrl] = None


