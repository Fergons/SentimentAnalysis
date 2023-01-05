from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.aspect import Aspect
from app.schemas.aspect import AspectCreate, AspectUpdate


class CRUDAspect(CRUDBase[Aspect, AspectCreate, AspectUpdate]):
    pass


crud_aspect = CRUDAspect(Aspect)
