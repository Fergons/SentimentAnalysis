from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession


from app import models, schemas
from app.crud.base import CRUDBase
from app.models.aspect import Aspect
from app.schemas.aspect import AspectCreate, AspectUpdate

from typing import List


class CRUDAspect(CRUDBase[Aspect, AspectCreate, AspectUpdate]):
    async def create_for_review(self, db: AsyncSession, *, obj_in: AspectCreate, review_id: int) -> Aspect:
        db_obj = Aspect(**obj_in.dict(), review_id=review_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, *, objs_in: List[AspectCreate]) -> List[Aspect]:
        db_objs = [Aspect(**obj.dict()) for obj in objs_in]
        db.add_all(db_objs)
        await db.commit()
        return db_objs

    async def get_most_mentioned_category(
            self, db: AsyncSession, *, game_id: int, model_id: str, limit: int = 10
    ) -> List[Aspect]:
        result = await db.execute(select(models.Aspect.category, func.count(models.Aspect.category))
                                  .filter(models.Aspect.model_id == model_id)
                                  .join(models.Review,
                                        and_(models.Review.id == models.Aspect.review_id,
                                             models.Review.game_id == game_id))
                                  .group_by(models.Aspect.category)
                                  .order_by(func.count(models.Aspect.category).desc()).limit(limit))
        return result.all()

    async def get_wordcloud(self, db: AsyncSession, *, game_id: int, model_id: str,
                            limit: int = 1000) -> schemas.AspectWordcloud:
        query = select(
            models.Aspect.category,
            models.Aspect.polarity,
            func.lower(models.Aspect.term),
            func.count(models.Aspect.id.distinct()).label('count')
        ).outerjoin(
            models.Review, models.Review.id == models.Aspect.review_id
        ).filter(
            models.Review.game_id == game_id,
            models.Aspect.model_id == model_id,
            models.Aspect.term != 'NULL'
        ).group_by(
            func.lower(models.Aspect.term),
            models.Aspect.category,
            models.Aspect.polarity
        ).order_by(
            func.count(models.Aspect.id.distinct()).desc(),
            models.Aspect.category,
            models.Aspect.polarity
        )
        result = await db.execute(query)

        wordcloud = schemas.AspectWordcloud(
            categories={}
        )

        for row in result.all():
            category, polarity, term, count = row
            if category not in wordcloud.categories:
                wordcloud.categories[category] = schemas.AspectTermPolarityGroups(
                    positive=[],
                    negative=[],
                    neutral=[]
                )
            getattr(wordcloud.categories[category], polarity).append((term, count))

        return wordcloud


crud_aspect = CRUDAspect(Aspect)
