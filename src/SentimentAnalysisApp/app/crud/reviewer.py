from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.reviewer import Reviewer
from app.schemas.reviewer import ReviewerCreate, ReviewerUpdate
from app.schemas.source import SourceBase
from app.crud.source import crud_source


class CRUDReviewer(CRUDBase[Reviewer, ReviewerCreate, ReviewerUpdate]):
    async def create_with_source_name(
            self, db: AsyncSession, *, obj_in: ReviewerCreate, source_name: str
    ) -> Optional[Reviewer]:
        obj_in_data = jsonable_encoder(obj_in)
        db_source = await crud_source.get_by_name(db, name=source_name)
        if db_source is None:
            return None
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.source = db_source
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_from_source(
            self, db: AsyncSession, *, obj_in: ReviewerCreate
    ) -> Optional[Reviewer]:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, *, objs_in: List[ReviewerCreate]):
        db_objs = []
        for obj in objs_in:
            db_obj = self.model(**obj.dict())  # type: ignore
            db_objs.append(db_obj)
        db.add_all(db_objs)
        await db.commit()

    async def get_ids_by_source_reviewer_ids(self, db: AsyncSession, *, source_id: int,
                                             source_reviewer_ids: List[str]) -> dict:
        result = await db.execute(
            select(self.model.source_reviewer_id, self.model.id)
            .where(
                and_(self.model.source_id == source_id,
                     self.model.source_reviewer_id.in_(source_reviewer_ids))))
        return dict(result.all())


crud_reviewer = CRUDReviewer(Reviewer)
