"""
Created by Frantisek Sabol
"""
from typing import List
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app import models, schemas
from .base import CRUDBase


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
            query = query.where(models.AnalyzedReview.created_at >= search_filter.created_at).order_by(
                models.AnalyzedReview.created_at.desc())
        if search_filter.updated_at:
            query = query.where(models.AnalyzedReview.updated_at >= search_filter.updated_at).order_by(
                models.AnalyzedReview.updated_at.desc())
        else:
            query = query.order_by(models.AnalyzedReview.id.desc(), models.AnalyzedReview.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()

    async def get_games_with_unprocessed_reviews(self, db: AsyncSession, limit: int = 100) -> List[models.Game]:
        """
        Get all games with unprocessed reviews
        :param db: AsyncSession
        :param limit: int
        :return: List[Game]
        """
        # select from table game where count of reviews with processed_at null values is > 0
        games_with_unprocessed_reviews = await db.execute(select(models.Game)
                                                          .join(models.Review, models.Game.id == models.Review.game_id)
                                                          .filter(models.Review.processed_at == None)
                                                          .group_by(models.Game.id)
                                                          .order_by(func.count(models.Review.id).desc())
                                                          .limit(limit))
        return games_with_unprocessed_reviews.scalars().all()


class CRUDAnalyzedReview(CRUDBase[models.AnalyzedReview, schemas.AnalyzedReviewCreate, schemas.AnalyzedReviewUpdate]):
    """
    CRUD facade for AnalyzedReview model
    """
    pass


class CRUDAnalyzedReviewSentence(CRUDBase[
                                     models.AnalyzedReviewSentence, schemas.AnalyzedReviewSentenceCreate, schemas.AnalyzedReviewSentenceUpdate]):
    """
    CRUD facade for AnalyzedReviewSentence model
    """
    pass


crud_analyzer = CRUDAnalyzer(models.AnalyzedReview)
crud_analyzed_review = CRUDAnalyzedReview(models.AnalyzedReview)
crud_analyzed_review_sentence = CRUDAnalyzedReviewSentence(models.AnalyzedReviewSentence)
