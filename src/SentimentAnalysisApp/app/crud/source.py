from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.source import Source, GameSource
from app.schemas.source import SourceCreate, SourceUpdate, GameSourceCreate, GameSourceUpdate


class CRUDGameSource(CRUDBase[GameSource, GameSourceCreate, GameSourceUpdate]):
    pass


class CRUDSource(CRUDBase[Source, SourceCreate, SourceUpdate]):
    async def create_with_url(
            self, db: AsyncSession, *, obj_in: SourceCreate, url: str,
    ) -> Source:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, url=url)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Source]:
        result = await db.execute(select(Source).where(Source.name == name))
        return result.scalars().first()

    async def get_by_url(self, db: AsyncSession, *, url: str) -> Optional[Source]:
        result = await db.execute(select(Source).where(Source.url == url))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[Source]:
        result = await db.execute(select(self.model))
        return result.scalars().all()


crud_source = CRUDSource(Source)
crud_game_source = CRUDGameSource(GameSource)
