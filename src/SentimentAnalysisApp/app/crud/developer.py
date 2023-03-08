from typing import List, Optional, Any, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import column, update, func, cast, and_, text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.db.session import RegConfig
from app.models.game import GameDeveloper, Game
from app.models.developer import Developer
from app.schemas.developer import DeveloperCreate, DeveloperUpdate


class CRUDDeveloper(CRUDBase[Developer, DeveloperCreate, DeveloperUpdate]):

    async def get_id_by_name(self, db: AsyncSession, *, name: str) -> Optional[int]:
        result = await db.scalars(select(self.model.id).where(self.model.name == name))
        return result.first()

    async def _add_developers_by_name_for_game(self, db: AsyncSession, *, db_game: Game, names: List[str]):
        result = await db.execute(select(self.model.name, self.model.id).where(self.model.name.in_(names)))
        developers_ids = result.all()
        developers_ids = {name: id for name, id in developers_ids}
        db_objs_to_add = []
        for name in names:
            dev_id = developers_ids.get(name)
            if dev_id is None:
                db_obj = Developer(name=name)  # type: ignore
                assoc = GameDeveloper(game=db_game)  # type: ignore
                db_obj.games.append(assoc)
                db_objs_to_add.append(db_obj)
                db_objs_to_add.append(assoc)
            else:
                assoc = GameDeveloper(game=db_game, developer_id=dev_id)  # type: ignore
                db_objs_to_add.append(assoc)
        db.add_all(db_objs_to_add)


crud_developer = CRUDDeveloper(Developer)
