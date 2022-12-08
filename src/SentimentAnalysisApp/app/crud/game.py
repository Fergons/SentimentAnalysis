import logging
from typing import List, Optional, Any, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import column, update, func, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.db.session import RegConfig
from app.crud.source import crud_source
from app.models.source import GameSource, Source
from app.models.game import Game, Category, GameCategory
from app.schemas.game import GameCreate, GameUpdate, GameCreate
from app.schemas.game import CategoryCreate, CategoryUpdate, CategoryBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]) :
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        result = await db.execute(select(self.model).where(self.model.name == name))
        return result.scalars().first()

    async def create_by_name_with_game_multi(self, db: AsyncSession, *, db_game: Game, names: List[str]):
        for name in names:
            db_obj = await self.get_by_name(db, name=name)
            if db_obj is None:
                db_obj = Category(name=name)  # type: ignore
            assoc = GameCategory(game=db_game)  # type: ignore
            db_obj.games.append(assoc)
            db.add(db_obj)
        await db.commit()


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]) :
    async def get_by_source_id(self, db: AsyncSession, source_id: Any, source_game_id: Any) -> Optional[Game]:
        result = await db.execute(select(GameSource).where((GameSource.source_id == source_id) &
                                                           (GameSource.source_game_id == str(source_game_id)))
                                  .options(selectinload(GameSource.game)))
        db_obj = result.scalars().first()
        if db_obj is None:
            return None
        return db_obj.game

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        ts_query = func.plainto_tsquery(cast("english", RegConfig), name)
        stmt = select(self.model).where(
            self.model.name_tsv.bool_op("@@")(ts_query)
        ).limit(5)

        result = await db.execute(stmt)
        return result.scalars().first()

    async def create_with_categories_by_names(
            self, db: AsyncSession, *, obj_in: GameCreate, names: List[str]
    ) -> Game:
        db_obj = self.model(**obj_in.dict(exclude={"source_id", "source_game_id"}))  # type: ignore
        await crud_category.create_by_name_with_game_multi(db, db_game=db_obj, names=names)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_categories_by_names_and_source(
            self, db: AsyncSession, *, obj_in: GameCreate, names: List[str]
    ) -> Optional[Game]:
        obj_in_data = obj_in.dict()
        game_db_obj = await self.create_with_categories_by_names(
            db,
            obj_in=GameCreate(**obj_in_data),
            names=names
        )
        game_source_db_obj = GameSource(
            game_id=game_db_obj.id,                # type: ignore
            source_id=obj_in.source_id,            # type: ignore
            source_game_id=obj_in.source_game_id   # type: ignore
        )
        db.add(game_source_db_obj)
        await db.commit()
        await db.refresh(game_db_obj)
        return game_db_obj


    async def get_all_db_games_from_source(self, db: AsyncSession, *, source_id: int) -> List[GameSource]:
        result = await db.execute(
            select(GameSource)
            .where(
                (GameSource.source_id == source_id) &
                (GameSource.game_id is not None)
            )
        )
        return result.scalars().all()

    async def get_all_not_updated_db_games_from_source(self, db: AsyncSession, *, source_id: int) -> List[GameSource]:
        result = await db.execute(
            select(GameSource, Game)
            .where(
                (GameSource.source_id == source_id) &
                (GameSource.game_id == Game.id) &
                (Game.updated_at is not None)
            )
            .options(selectinload(GameSource.game))
        )
        return result.scalars().all()

    async def get_all_app_ids_from_source(self, db: AsyncSession, *, source_id: int) -> List[int]:
        result = await db.execute(select(GameSource.source_game_id).where(GameSource.source_id == source_id))
        return result.scalars().all()

    async def create_non_game_app_from_source(self, db: AsyncSession, *,
                                              source_id: int, source_obj_id: Any):
        game_source_db_obj = GameSource(
            source_id=source_id,            # type: ignore
            source_game_id=str(source_obj_id)   # type: ignore
        )
        db.add(game_source_db_obj)
        await db.commit()

    async def create_from_source(self, db: AsyncSession, *,
                                 obj_in: GameCreate):
        game_source_db_obj = GameSource(
            source_id=obj_in.source_id,            # type: ignore
            source_game_id=str(obj_in.source_game_id)   # type: ignore
        )
        db_obj = Game(**obj_in.dict(exclude={"source_id", "source_game_id"}))  # type: ignore
        game_source_db_obj.game_id = db_obj.id
        db.add(db_obj)
        db.add(game_source_db_obj)
        await db.commit()



crud_game = CRUDGame(Game)
crud_category = CRUDCategory(Category)
