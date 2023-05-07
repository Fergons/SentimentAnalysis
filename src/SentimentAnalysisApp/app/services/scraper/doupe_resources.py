"""
Created by Frantisek Sabol
Doupe.cz scraper resources used for data validation and transformation
"""
from typing import Optional, List

from pydantic import BaseModel, Field

MAX_PAGE = 90
MAX_PER_PAGE = 36

game_tags = {
    "tag-Akce": "Action",
    "tag-Adventury": "Adventure",
    "tag-Plošinovky": "Platform",
    "tag-Strategie": "Strategy",
    "tag-Simulatory": "Simulation",
    "tag-Závodní": "Racing",
    "tag-RPG": "RPG",
    "tag-FPS": "FPS"
}


class DoupeReviewsRequestParams(BaseModel):
    pgnum: int = 1


class DoupeReviewer(BaseModel):
    source_reviewer_id: str = Field(alias="source_reviewer_id")
    name: str = ""
    class Config:
        allow_population_by_field_name = True

class DoupeGame(BaseModel):
    url: str = Field(alias="source_game_id")
    name: str = ""
    tags: Optional[List[str]] = None
    class Config:
        allow_population_by_field_name = True

class DoupeReview(BaseModel):
    url: str = Field(alias="source_review_id")
    score: Optional[str] = None
    text: str = ""
    good: Optional[str] = None
    bad: Optional[str] = None
    source_reviewer_id: Optional[str] = None
    tags: Optional[List[str]] = None
    language: str = "czech"

    class Config:
        allow_population_by_field_name = True
