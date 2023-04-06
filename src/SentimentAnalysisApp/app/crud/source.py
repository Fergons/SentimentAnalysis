import datetime
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import CRUDBase
from app import schemas, models

class CRUDGameSource(CRUDBase[models.GameSource, schemas.GameSourceCreate, schemas.GameSourceUpdate]):
    async def log_review_scraping(self, db: AsyncSession, *, game_id: int, source_id: int, scraped_at: datetime.datetime) -> models.GameSource:
        result = await db.execute(select(models.GameSource).where(
            models.GameSource.game_id == game_id,
            models.GameSource.source_id == source_id
        ).options(selectinload(models.GameSource.game), selectinload(models.GameSource.source)))
        game_source = result.scalars().first()
        if game_source is None:
            raise ValueError(f"GameSource for game_id: {game_id} and source_id: {source_id} not found")
        game_source.reviews_scraped_at = scraped_at
        await db.commit()
        return game_source


class CRUDSource(CRUDBase[models.Source, schemas.SourceCreate, schemas.SourceUpdate]):
    async def create_with_url(
            self, db: AsyncSession, *, obj_in: schemas.SourceCreate, url: str,
    ) -> models.Source:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, url=url)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[models.Source]:
        result = await db.execute(select(self.model).where(self.model.name == name))
        return result.scalars().first()

    async def get_by_url(self, db: AsyncSession, *, url: str) -> Optional[models.Source]:
        result = await db.execute(select(self.model).where(self.model.url == url))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[models.Source]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def add_game(self, db: AsyncSession, *, game_id: Optional[int] = None, source_id: int, source_game_id: str
                       ) -> models.GameSource:
        db_obj = models.GameSource(game_id=game_id, source_id=source_id, source_game_id=source_game_id)
        db.add(db_obj)
        await db.commit()
        return db_obj


crud_source = CRUDSource(models.Source)
crud_game_source = CRUDGameSource(models.GameSource)
