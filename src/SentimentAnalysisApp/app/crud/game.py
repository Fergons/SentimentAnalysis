import logging
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.crud.source import crud_source
from app.models.source import GameSource, Source
from app.models.game import Game, Category, GameCategory
from app.schemas.game import GameCreate, GameUpdate, GameFromSourceCreate, GameFromSourceUpdate
from app.schemas.game import CategoryCreate, CategoryUpdate, CategoryBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]) :
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category] :
        result = await db.execute(select(Category).where(Category.name == name))
        return result.scalars().first()


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]) :
    async def create_with_categories_by_names(
            self, db: AsyncSession, *, obj_in: GameCreate, categories_by_names: List[str]
    ) -> Game :
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.release_date = obj_in.release_date
        for name in categories_by_names :
            result = await db.execute(
                select(Category).where(Category.name == name).options(selectinload(Category.games)))
            new_c = result.scalars().first()
            if new_c is None :
                new_c = await crud_category.create(db, obj_in=CategoryCreate(name=name))
            if new_c is not None :
                new_assoc = GameCategory()
                new_assoc.game = db_obj
                new_c.games.append(new_assoc)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_categories_by_names_and_source(
            self, db: AsyncSession, *, obj_in: GameFromSourceCreate, categories_by_names: List[str]
    ) -> Optional[Game] :
        game_db_obj = await self.create_with_categories_by_names(
            db, obj_in=GameCreate(**obj_in.dict()), categories_by_names=categories_by_names)
        game_source_db_obj = GameSource(source_game_id=obj_in.source_game_id)  # type: ignore
        result = await db.execute(
            select(Source).where(Source.id == obj_in.source_id).options(selectinload(Source.games)))
        source_db_obj = result.scalars().first()
        if source_db_obj is None:
            return None
        game_source_db_obj.game = game_db_obj
        game_source_db_obj.source = source_db_obj
        source_db_obj.games.append(game_source_db_obj)

        await db.commit()
        await db.refresh(game_db_obj)
        await db.refresh(game_source_db_obj)
        await db.refresh(source_db_obj)

        return game_db_obj


crud_game = CRUDGame(Game)
crud_category = CRUDCategory(Category)
