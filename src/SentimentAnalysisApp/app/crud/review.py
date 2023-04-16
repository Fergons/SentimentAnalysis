import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Literal, Tuple, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_, or_, func, literal_column, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql.expression import null, text

from app.crud.reviewer import crud_reviewer
from app.crud.base import CRUDBase
from app.schemas.review import (ReviewCreate, ReviewWithAspects,
                                ReviewsSummary, ReviewsSummaryDataPoint)
from app.schemas.reviewer import ReviewerCreate

from app.crud.game import crud_game
from app import models, schemas

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)


class CRUDReview(CRUDBase[models.Review, ReviewCreate, ReviewCreate]):
    async def get_with_good_and_bad_by_language_multi(self, db: AsyncSession, *, language: str) -> List[models.Review]:
        result = await db.execute(
            select(self.model).where(and_(self.model.language == language,
                                          or_(self.model.good != None, self.model.bad != None)
                                          )
                                     )
        )

        return result.scalars().all()

    async def get_by_user(self, db: AsyncSession, *, user_id: int) -> List[models.Review]:
        result = await db.execute(select(self.model).where(self.model.reviewer_id == user_id))
        return result.scalars().all()

    async def get_multi_by_game(self, db: AsyncSession, *, game_id: int, limit: int = 100, offset: int = 0
                                ) -> List[models.Review]:
        result = await db.execute(select(self.model).where(self.model.game_id == game_id))
        return result.scalars().all()

    async def get_multi_by_game_and_source(self, db: AsyncSession, *,
                                           source_id: Optional[int] = None,
                                           game_id: Optional[int] = None,
                                           limit: int = 100,
                                           offset: int = 0
                                           ) -> List[models.Review]:
        query = select(self.model).limit(limit).offset(offset)
        if game_id is not None:
            query = query.filter(self.model.game_id == game_id)
        if source_id is not None:
            query = query.filter(self.model.source_id == source_id)
        result = await db.execute(
            query.order_by(self.model.created_at.desc()).options(selectinload(self.model.aspects)))
        return result.scalars().all()

    async def get_multi_by_processed(self, db: AsyncSession, *, processed: bool, limit: int = 100, offset: int = 0) -> \
            List[models.Review]:
        if processed:
            result = await db.execute(
                select(self.model).where(self.model.processed_at != None).limit(limit).offset(offset))
        else:
            result = await db.execute(
                select(self.model).where(self.model.processed_at == None).limit(limit).offset(offset))
        return result.scalars().all()

    async def get_multi_with_aspects(self, db: AsyncSession, *,
                                     aspects: List[str] = None,
                                     model_ids: List[str] = None,
                                     game_id: int = None,
                                     polarities: List[str] = None,
                                     limit: int = 100,
                                     offset: int = 0) -> schemas.ReviewListResponse:
        count = select(func.count(self.model.id)).filter(self.model.processed_at != None)
        query = select(self.model).filter(self.model.processed_at != None)

        # Join the models.Aspect table and filter by aspects
        query = query.join(models.Aspect, models.Aspect.review_id == self.model.id)
        count = count.join(models.Aspect, models.Aspect.review_id == self.model.id)

        if model_ids is not None:
            query = query.filter(models.Aspect.model_id.in_(model_ids))
            count = count.filter(models.Aspect.model_id.in_(model_ids))

        if aspects is not None:
            query = query.filter(models.Aspect.category.in_(aspects))
            count = count.filter(models.Aspect.category.in_(aspects))

        # Filter by polarities if provided
        if polarities is not None:
            query = query.filter(models.Aspect.polarity.in_(polarities))
            count = count.filter(models.Aspect.polarity.in_(polarities))

        if game_id is not None:
            query = query.filter(self.model.game_id == game_id)
            count = count.filter(self.model.game_id == game_id)

        result = await db.execute(
            query.group_by(self.model.id).order_by(self.model.id)
            .options(
                selectinload(self.model.aspects)
            ).limit(limit).offset(offset)
        )
        reviews = result.scalars().all()
        result = await db.execute(count.group_by(self.model.id))
        total = result.scalar() or 0
        return schemas.ReviewListResponse(reviews=reviews, total=total)

    async def get_summary(self, db: AsyncSession, *,
                          game_id: Optional[int] = None,
                          source_id: Optional[int] = None,
                          time_interval: Literal["day", "hour", "month", "year"] = "day") -> ReviewsSummary:
        """
        Count total reviews, count processed and not processed reviews per game and source by time_interval
        """
        summary = ReviewsSummary()
        query = select(
            func.array_agg(self.model.id).label('ids'),
            func.array_agg(case(
                [(self.model.voted_up == True, self.model.id)])).label("positive"),
            func.array_agg(case(
                [(self.model.processed_at != None, self.model.id)])).label("processed"),
            func.date_trunc(time_interval, self.model.created_at).label('date'),
            self.model.source_id
        ) \
            .group_by('date', self.model.source_id) \
            .order_by(text('date desc'))

        if game_id is not None:
            query = query.filter(self.model.game_id == game_id)
            summary.game_id = game_id

        result = await db.execute(query)
        data = result.all()
        data_points = []
        for all_ids, positive_ids, processed_ids, date, source_id in data:
            data_point = ReviewsSummaryDataPoint(total=len(all_ids),
                                                 processed=len([i for i in processed_ids if i is not None]),
                                                 positive=len([i for i in positive_ids if i is not None]),
                                                 date=date,
                                                 source_id=source_id)
            data_points.append(data_point)

        summary.data = data_points
        summary.num_data_points = len(data_points)
        return summary

    async def get_summary_v2(
            self, db: AsyncSession, *, game_id: int, time_interval: str = "day", model: str = "mt5-acos-1.0"
    ) -> schemas.ReviewsSummaryV2:
        """
        Count total reviews, count processed and not processed reviews per game and source by time_interval
        """
        query = select(
            func.date_trunc(time_interval, models.Review.created_at).label('date'),
            models.Review.source_id,
            func.count(func.distinct(models.Review.id)).label("total"),
            func.count(func.distinct(case([(models.Review.processed_at == None, models.Review.id)]))).label(
                "not_processed"),
            func.count(func.distinct(case([(models.Review.processed_at != None, models.Review.id)]))).label(
                "processed"),
            func.sum(case([(models.Aspect.polarity == "positive", 1)], else_=0)).label("positive"),
            func.sum(case([(models.Aspect.polarity == "negative", 1)], else_=0)).label("negative"),
            func.sum(case([(models.Aspect.polarity == "neutral", 1)], else_=0)).label("neutral")
        )
        if game_id is not None:
            query = query.filter(models.Review.game_id == game_id)

        result = await db.execute(
            query.outerjoin(models.Aspect, models.Review.id == models.Aspect.review_id)
            .filter((models.Aspect.model_id == model) | (models.Aspect.id == None)
                    )
            .group_by(text("date"), models.Review.source_id)
            .order_by(text("date"), models.Review.source_id)
        )

        summary = schemas.ReviewsSummaryV2(
            total=0,
            not_processed=0,
            processed=0,
            positive=0,
            negative=0,
            neutral=0,
            data={},
        )
        current_date = None
        current_date_summary = None

        for row in result.all():
            date, source_id, total, not_processed, processed, positive, negative, neutral = row
            summary.total += total
            summary.not_processed += not_processed
            summary.processed += processed
            summary.positive += positive
            summary.negative += negative
            summary.neutral += neutral

            if date != current_date:
                if current_date_summary:
                    summary.data[current_date] = current_date_summary

                current_date = date
                current_date_summary = schemas.ReviewsSummaryByDate(
                    total=0,
                    not_processed=0,
                    processed=0,
                    positive=0,
                    negative=0,
                    neutral=0,
                    sources={},
                )

            current_date_summary.total += total
            current_date_summary.not_processed += not_processed
            current_date_summary.processed += processed
            current_date_summary.positive += positive
            current_date_summary.negative += negative
            current_date_summary.neutral += neutral

            if source_id not in current_date_summary.sources:
                current_date_summary.sources[source_id] = schemas.ReviewsSummaryBaseDataPoint(
                    total=0,
                    processed=0,
                    not_processed=0,
                    positive=0,
                    negative=0,
                    neutral=0,
                )

            current_date_summary.sources[source_id].total += total
            current_date_summary.sources[source_id].not_processed += not_processed
            current_date_summary.sources[source_id].processed += processed
            current_date_summary.sources[source_id].positive += positive
            current_date_summary.sources[source_id].negative += negative
            current_date_summary.sources[source_id].neutral += neutral

        if current_date_summary:
            summary.data[current_date] = current_date_summary

        return summary

    async def get_not_processed(self, db: AsyncSession, *, limit: int = 100, offset: int = 0) -> List[models.Review]:
        result = await db.execute(select(self.model).where(self.model.processed_at == None).limit(limit).offset(offset))
        return result.scalars().all()

    async def count_not_processed_reviews(self, db: AsyncSession, **kwargs) -> int:
        """
        Get number of not processed reviews by search filter
        """
        conditions = []
        for key, value in kwargs.items():
            if value is not None:
                conditions.append(getattr(self.model, key) == value)
        query = select(func.count(self.model.id)).where(and_(self.model.processed_at == None, *conditions))
        result = await db.execute(query)
        return result.scalar()

    async def count_filtered_reviews(self, db: AsyncSession, **kwargs) -> int:
        conditions = []
        for key, value in kwargs.items():
            if value is not None:
                conditions.append(getattr(self.model, key) == value)
        query = select(func.count(self.model.id)).where(and_(*conditions))
        result = await db.execute(query)
        return result.scalar()

    async def get_not_processed_by_game(self, db: AsyncSession, game_id: int, limit: int = 100, last_id: int = None) -> \
            List[models.Review]:
        if last_id:
            result = await db.execute(
                select(self.model)
                .where((self.model.id > last_id) & (self.model.processed_at == None) & (self.model.game_id == game_id))
                .limit(limit)
                .order_by(self.model.id.asc()))
        else:
            result = await db.execute(
                select(self.model)
                .where((self.model.processed_at == None) & (self.model.game_id == game_id))
                .limit(limit)
                .order_by(self.model.id.asc()))

        return result.scalars().all()

    async def get_not_processed_by_source(self, db: AsyncSession,
                                          source_id: int,
                                          limit: int = 100,
                                          offset: int = 0) -> Optional[models.Review]:

        if offset > 2000:
            stmt = select(self.model.id) \
                .where((self.model.processed_at == None) & (self.model.source_id == source_id)) \
                .limit(limit).offset(offset)
            result_ids = await db.execute(stmt)
            ids = result_ids.scalars().all()
            stmt = select(self.model).where(self.model.id.in_(ids))
        else:
            stmt = select(self.model).where((self.model.processed_at == None) & (self.model.source_id == source_id)) \
                .limit(limit).offset(offset)

        result = await db.execute(stmt)
        return result.scalars().all()

    async def create_with_text(
            self, db: AsyncSession, *, obj_in: ReviewCreate, text: str
    ) -> models.Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, text=text)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_reviewer(
            self, db: AsyncSession, *, obj_in: ReviewCreate, text: str,
    ) -> models.Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, text=text)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, *, objs_in: List[ReviewCreate], limit: int = 100):
        db_objs = []
        for obj in objs_in:
            logger.debug(f"create_multi: Checking if review {obj.source_review_id} in db")
            db_obj_id = await self.get_id_by_source_id(db, obj.source_id, obj.source_review_id)
            logger.debug(f"create_multi: review {obj.source_review_id}: {'FOUND' if db_obj_id else 'NOT FOUND'}")
            if db_obj_id is not None:
                # possible update of the review in the DB
                continue
            db_obj = self.model(**obj.dict())  # type: ignore
            db_objs.append(db_obj)

        db.add_all(db_objs)
        await db.commit()

    async def create_with_reviewer_multi(
            self, db: AsyncSession, *,
            objs_in: List[ReviewCreate],
            reviewers_in: List[ReviewerCreate],
            limit: int = 100):

        for review_obj, reviewer_obj in zip(objs_in, reviewers_in):
            db_obj = await self.get_by_source_id(db, review_obj.source_id, review_obj.source_review_id)
            if db_obj is not None:
                # possible update of the review in the DB
                continue
            reviewer_db_obj = await crud_reviewer.get_by_source_id(db, reviewer_obj.source_id,
                                                                   reviewer_obj.source_reviewer_id)
            if reviewer_db_obj is None:
                reviewer_db_obj = Reviewer(**reviewer_obj.dict())  # type: ignore
                db.add(reviewer_db_obj)
            db_obj = self.model(**review_obj.dict())  # type: ignore
            db_obj.reviewer = reviewer_db_obj
            db.add(db_obj)

        await db.commit()

    async def create_with_game_multi(
            self, db: AsyncSession, *,
            objs_in: List[ReviewCreate]
    ):

        for obj in objs_in:
            db_obj = await self.get_by_source_id(db, obj.source_id, obj.source_review_id)
            if db_obj is not None:
                # possible update of the review in the DB
                continue

            db_obj = self.model(**obj.dict())  # type: ignore
            db.add(db_obj)

        await db.commit()

    async def get_with_aspects(self, db: AsyncSession, *, id: int) -> Optional[models.Review]:
        result = await db.execute(select(self.model).where(self.model.id == id).options(
            selectinload(self.model.aspects)
        ))
        return result.scalars().first()

    async def get_ids_by_source_review_ids(self, db: AsyncSession, source_id: int,
                                           source_review_ids: List[str]) -> dict:
        result = await db.execute(
            select(self.model.source_review_id, self.model.id)
            .where(and_(self.model.source_id == source_id, self.model.source_review_id.in_(source_review_ids))))
        return dict(result.all())

    async def get_ids_and_text(self, db: AsyncSession, *, source_id: int, offset: int = 0, limit: int = 100) -> List[
        Tuple[int, str]]:
        result = await db.scalars(
            select(self.model.id, self.model.text)
            .where(self.model.source_id == source_id)
            .order_by(self.model.id).limit(1000))
        return result.all()

    async def get_aspect_summary_by_category_and_sources(
            self, db: AsyncSession, *, game_id: int = None, model: str = "mt5-acos-1.0"
    ) -> schemas.AspectsSummary:
        query = select(
            models.Review.source_id,
            models.Aspect.category,
            models.Aspect.polarity,
            func.count(models.Aspect.id).label("count")
        ).outerjoin(
            models.Aspect, models.Review.id == models.Aspect.review_id
        ).filter(
            models.Aspect.model_id == model
        )

        if game_id is not None:
            query = query.filter(models.Review.game_id == game_id)

        query = query.group_by(
            models.Review.source_id,
            models.Aspect.category,
            models.Aspect.polarity
        )

        result = await db.execute(query)

        summary = schemas.AspectsSummary(
            total=schemas.PolarityCounts(positive=0, negative=0, neutral=0),
            sources={},
            dates={}
        )

        for row in result.all():
            source_id, category, polarity, count = row
            if source_id not in summary.sources:
                summary.sources[source_id] = schemas.CategoryPolarityCounts(
                    total=schemas.PolarityCounts(positive=0, negative=0, neutral=0),
                    categories={}
                )

            source_summary = summary.sources[source_id]
            setattr(source_summary.total, polarity, getattr(source_summary.total, polarity) + count)

            if category not in source_summary.categories:
                source_summary.categories[category] = schemas.PolarityCounts(positive=0, negative=0, neutral=0)

            setattr(source_summary.categories[category], polarity,
                    getattr(source_summary.categories[category], polarity) + count)
            setattr(summary.total, polarity, getattr(summary.total, polarity) + count)

        return summary

    async def get_aspects_summary_by_date_and_categories(
            self, db: AsyncSession, *, game_id: int, time_interval: str = "day", model: str = "mt5-acos-1.0"
    ) -> schemas.AspectsSummary:
        query = select(
            func.date_trunc(time_interval, models.Review.created_at).label("date"),
            models.Aspect.category,
            models.Aspect.polarity,
            func.count(models.Aspect.id).label("count")
        ).outerjoin(
            models.Aspect, models.Review.id == models.Aspect.review_id
        ).filter(
            models.Review.game_id == game_id,
            models.Aspect.model_id == model
        ).group_by(
            "date",
            models.Aspect.category,
            models.Aspect.polarity
        ).order_by(
            "date"
        )

        result = await db.execute(query)

        summary = schemas.AspectsSummary(
            total=schemas.PolarityCounts(positive=0, negative=0, neutral=0),
            sources={},
            dates={}
        )

        for row in result.all():
            date, category, polarity, count = row

            if date not in summary.dates:
                summary.dates[date] = schemas.CategoryPolarityCounts(
                    total=schemas.PolarityCounts(positive=0, negative=0, neutral=0),
                    categories={}
                )

            date_summary = summary.dates[date]
            setattr(date_summary.total, polarity, getattr(date_summary.total, polarity) + count)

            if category not in date_summary.categories:
                date_summary.categories[category] = schemas.PolarityCounts(positive=0, negative=0, neutral=0)
            setattr(date_summary.categories[category], polarity,
                    getattr(date_summary.categories[category], polarity) + count)
            setattr(summary.total, polarity, getattr(summary.total, polarity) + count)

        return summary


crud_review = CRUDReview(models.Review)
