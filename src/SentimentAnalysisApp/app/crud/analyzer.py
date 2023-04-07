import logging
from datetime import timedelta, datetime
from typing import List, Optional, Any, Tuple, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import column, update, func, cast, and_, text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from app import models, schemas
from .base import CRUDBase
from .game import crud_game
from .game import crud_category
from .developer import crud_developer
from .review import crud_review
from .reviewer import crud_reviewer
from .source import crud_source


class CRUDAnalyzer(CRUDBase[models.AnalyzedReview, schemas.AnalyzedReviewCreate, schemas.AnalyzedReviewUpdate]):
    """
    Analyzer specific CRUD facade for Aspect Based Sentiment Analysis module
    app.services.analyzer.acos
    """

    async def get_analyzed_reviews(self, db: AsyncSession, search_filter: schemas.AnalyzerSearchFilter) -> List[
        models.AnalyzedReview]:
        """
        Get all analyzed reviews from the database
        :param db: AsyncSession
        :param search_filter: AnalyzerSearchFilter
        :return: List[AnalyzedReview]
        """
        query = select(models.AnalyzedReview).options(
            selectinload(models.AnalyzedReview.review),
            selectinload(models.AnalyzedReview.analyzed_review_sentences)
        )

        filter_map = {
            'task': models.AnalyzedReview.task,
            'model': models.AnalyzedReview.model,
            'prediction': models.AnalyzedReview.prediction,
            'gold_label': models.AnalyzedReview.gold_label,
            'review_id': models.AnalyzedReview.review_id,
            'analyzed_review_id': models.AnalyzedReview.id
        }

        for attr, model_attr in filter_map.items():
            value = getattr(search_filter, attr)
            if value:
                query = query.where(model_attr == value)

        if search_filter.created_at:
            query = query.where(models.AnalyzedReview.created_at >= search_filter.created_at).order_by(models.AnalyzedReview.created_at.desc())
        if search_filter.updated_at:
            query = query.where(models.AnalyzedReview.updated_at >= search_filter.updated_at).order_by(models.AnalyzedReview.updated_at.desc())
        else:
            query = query.order_by(models.AnalyzedReview.id.desc(), models.AnalyzedReview.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()


class CRUDAnalyzedReview(CRUDBase[models.AnalyzedReview, schemas.AnalyzedReviewCreate, schemas.AnalyzedReviewUpdate]):
    """
    CRUD facade for AnalyzedReview model
    """
    pass


class CRUDAnalyzedReviewSentence(CRUDBase[models.AnalyzedReviewSentence, schemas.AnalyzedReviewSentenceCreate, schemas.AnalyzedReviewSentenceUpdate]):
    """
    CRUD facade for AnalyzedReviewSentence model
    """
    pass


crud_analyzer = CRUDAnalyzer(models.AnalyzedReview)
crud_analyzed_review = CRUDAnalyzedReview(models.AnalyzedReview)
crud_analyzed_review_sentence = CRUDAnalyzedReviewSentence(models.AnalyzedReviewSentence)

