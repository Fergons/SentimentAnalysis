import logging
from datetime import timedelta, datetime
from typing import List, Optional, Any, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import column, update, func, cast, and_, text, or_
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
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        logging.debug(f"get_by_name: getting category {name} from db")
        result = await db.execute(select(self.model).where(self.model.name == name))
        logging.debug(f"get_by_name: got category {name} from db")
        return result.scalars().first()

    async def get_id_by_name(self, db: AsyncSession, *, name: str) -> Optional[int]:
        logging.debug(f"get_id_by_name: getting category {name} from db")
        result = await db.scalars(select(self.model.id).where(self.model.name == name))
        logging.debug(f"get_by_name: got category {name} from db")
        return result.first()

    async def create_by_name_with_game_multi(self, db: AsyncSession, *, db_game: Game, names: List[str]):
        for name in names:
            db_obj = await self.get_by_name(db, name=name)
            if db_obj is None:
                db_obj = Category(name=name)  # type: ignore
            assoc = GameCategory(game=db_game)  # type: ignore
            db_obj.games.append(assoc)
            db.add(db_obj)

        await db.commit()

    async def add_categories_by_name_for_game(self, db: AsyncSession, *, db_game: Game, names: List[str]):
        result = await db.execute(select(self.model.name, self.model.id).where(self.model.name.in_(names)))
        category_ids = result.all()
        category_ids = {name: id for name, id in category_ids}
        db_objs_to_add = []
        for name in names:
            id = category_ids.get(name)
            if id is None:
                db_obj = Category(name=name)  # type: ignore
                assoc = GameCategory(game=db_game)  # type: ignore
                db_obj.games.append(assoc)
                db_objs_to_add.append(db_obj)
                db_objs_to_add.append(assoc)
            else:
                assoc = GameCategory(game=db_game, category_id=id)  # type: ignore
                db_objs_to_add.append(assoc)
        db.add_all(db_objs_to_add)


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    async def get_by_source_id(self, db: AsyncSession, source_id: int, source_game_id: Any) -> Optional[Game]:
        result = await db.execute(select(GameSource.game_id).where(and_(GameSource.source_id == source_id,
                                                                        GameSource.source_game_id == str(source_game_id)
                                                                        )
                                                                   )
                                  )
        game_id = result.scalars().first()
        if game_id is None:
            return None
        result = await db.execute(select(self.model).where(self.model.id == game_id))
        db_obj = result.scalars().first()
        return db_obj

    async def get_ids_by_source_game_ids(self, db: AsyncSession, source_id: int, source_game_ids: List[str]) -> dict:
        result = await db.execute(select(GameSource.source_game_id, GameSource.game_id)
                                  .where(and_(GameSource.source_id == source_id,
                                              GameSource.source_game_id.in_(source_game_ids))))
        game_ids = result.all()
        if game_ids is None:
            return {}
        return dict(game_ids)

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        ts_query = func.plainto_tsquery(cast("english", RegConfig), name)
        stmt = select(self.model).where(
            self.model.name_tsv.bool_op("@@")(ts_query)
        ).limit(5)

        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_source_game_id(self, db: AsyncSession, *, id: int) -> str:
        result = await db.scalars(select(GameSource.source_game_id).where(GameSource.game_id == id))
        return result.first()

    async def create_from_source(self, db: AsyncSession, *, obj_in: GameCreate, source_id: int, source_game_id: str) -> Game:
        db_obj = self.model(**obj_in.dict()) # type: ignore

        assoc = GameSource(
            game=db_obj,  # type: ignore
            source_id=source_id,  # type: ignore
            source_game_id=source_game_id  # type: ignore
        )
        db.add_all([assoc, db_obj])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


    async def create_with_categories_by_names(
            self, db: AsyncSession, *, obj_in: GameCreate, names: List[str]
    ) -> Game:
        db_obj = self.model(**obj_in.dict(exclude={"source_id", "source_game_id"}))  # type: ignore
        logger.debug(f"creating categories for {obj_in.name}")
        await crud_category.add_categories_by_name_for_game(db, db_game=db_obj, names=names)
        logger.debug(f"created categories for {obj_in.name}")
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_categories_by_names_and_source(
            self, db: AsyncSession, *, obj_in: GameCreate, source_id: int, source_game_id: Any, names: List[str]
    ) -> Optional[Game]:
        obj_in_data = obj_in.dict()
        game_db_obj = self.model(**obj_in_data)  # type: ignore
        logger.debug(f"creating categories for {obj_in.name}")
        await crud_category.add_categories_by_name_for_game(db, db_game=game_db_obj, names=names)
        logger.debug(f"created categories for {obj_in.name}")
        game_source_db_obj = GameSource(
            game=game_db_obj,  # type: ignore
            source_id=source_id,  # type: ignore
            source_game_id=str(source_game_id)  # type: ignore
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
                (GameSource.game_id != None)
            )
        )
        return result.scalars().all()

    async def get_all_not_updated_db_games_from_source(self, db: AsyncSession, *,
                                                       source_id: int,
                                                       check_interval: timedelta = None) -> List[GameSource]:
        if check_interval is None:
            check_interval = timedelta(days=1)
        check_time = datetime.now() - check_interval
        result = await db.execute(
            select(Game.id, GameSource.source_game_id)
            .where(
                (Game.id == GameSource.game_id) &
                (GameSource.source_id == source_id) &
                or_(Game.updated_at == None, Game.updated_at <= check_time)
            )
        )
        return result.all()

    async def get_all_app_ids_from_source(self, db: AsyncSession, *, source_id: int) -> List[int]:
        result = await db.execute(select(GameSource.source_game_id).where(GameSource.source_id == source_id))
        return result.scalars().all()

    async def create_non_game_app_from_source(self, db: AsyncSession, *,
                                              source_id: int, source_obj_id: Any):
        game_source_db_obj = GameSource(
            source_id=source_id,  # type: ignore
            source_game_id=str(source_obj_id)  # type: ignore
        )
        db.add(game_source_db_obj)
        await db.commit()

    async def create_from_source(self, db: AsyncSession, *,
                                 obj_in: GameCreate,
                                 source_id: int,
                                 source_game_id: Any) -> Optional[Game]:
        db_obj = await self.get_by_source_id(db,
                                             source_id=source_id,
                                             source_game_id=source_game_id)
        if db_obj is not None:
            return db_obj

        db_obj = await self.get_by_name(db, name=obj_in.name)
        if db_obj is None:
            # db_obj = await self.create_with_categories_by_names_and_source(db,
            #                                                                obj_in=obj_in,
            #                                                                names=[c.name for c in obj_in.categories])
            db_obj = Game(**obj_in.dict(exclude={"source_id", "source_game_id", "categories"}))  # type: ignore
            db.add(db_obj)

        game_source_db_obj = GameSource(source_id=source_id,  # type: ignore
                                        source_game_id=str(source_game_id))  # type: ignore
        game_source_db_obj.game = db_obj
        db.add(game_source_db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_game = CRUDGame(Game)
crud_category = CRUDCategory(Category)
