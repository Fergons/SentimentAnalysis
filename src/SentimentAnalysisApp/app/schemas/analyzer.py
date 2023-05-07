"""
Created by Frantisek Sabol
This module contains the schemas for the analyzer module.
"""
from typing import Optional, List, Union, TYPE_CHECKING
from pydantic import BaseModel, AnyHttpUrl, Field, validator
from datetime import datetime


class AnalyzedReviewBase(BaseModel):
    review_id: int
    cleaned_text: str
    model: str
    task: str
    prediction: str
    gold_label: str


class AnalyzedReviewCreate(AnalyzedReviewBase):
    created_at: datetime
    gold_label: Optional[str] = None


class AnalyzedReviewUpdate(AnalyzedReviewCreate):
    review_id: Optional[int] = None
    cleaned_text: Optional[str] = None
    model: Optional[str] = None
    prediction: Optional[str] = None
    gold_label: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: datetime = datetime.now()


class AnalyzedReviewInDBBase(AnalyzedReviewBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AnalyzedReview(AnalyzedReviewInDBBase):
    pass


class AnalyzedReviewSentenceBase(BaseModel):
    sentence: str
    prediction: str
    gold_label: str
    analyzed_review_id: int


class AnalyzedReviewSentenceCreate(AnalyzedReviewSentenceBase):
    created_at: datetime = datetime.now()


class AnalyzedReviewSentenceUpdate(AnalyzedReviewSentenceCreate):
    sentence: Optional[str] = None
    prediction: Optional[str] = None
    gold_label: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: datetime = datetime.now()
    analyzed_review_id: Optional[int] = None


class AnalyzedReviewSentenceInDBBase(AnalyzedReviewBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AnalyzedReviewSentence(AnalyzedReviewSentenceInDBBase):
    pass


class AnalyzerSearchFilter(BaseModel):
    task: Optional[str] = None
    model: Optional[str] = None
    prediction: Optional[str] = None
    gold_label: Optional[str] = None
    review_id: Optional[int] = None
    analyzed_review_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AnalyzedReviewListResponse(BaseModel):
    reviews: List[AnalyzedReview]
    total: int