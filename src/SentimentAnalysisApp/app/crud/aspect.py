from sqlalchemy.ext.asyncio import AsyncSession

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


crud_aspect = CRUDAspect(Aspect)
