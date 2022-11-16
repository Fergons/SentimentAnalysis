from typing import List, Optional
from fastapi.encoders import jsonable_encoder
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


reviewer = CRUDReviewer(Reviewer)
