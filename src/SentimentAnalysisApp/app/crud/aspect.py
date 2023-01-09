from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.aspect import Aspect
from app.schemas.aspect import AspectCreate, AspectUpdate


class CRUDAspect(CRUDBase[Aspect, AspectCreate, AspectUpdate]):
    async def create_for_review(self, db: AsyncSession, *, obj_in: AspectCreate, review_id: int) -> Aspect:
        db_obj = Aspect(**obj_in.dict(), review_id=review_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_aspect = CRUDAspect(Aspect)
