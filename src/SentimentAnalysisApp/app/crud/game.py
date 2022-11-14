from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.game import Game
from app.schemas.game import GameCreate, GameCreate


class CRUDGame(CRUDBase[Game, GameCreate, GameCreate]):
    def create_with_name(
            self, db: Session, *, obj_in: GameCreate, name:str,
    ) -> Game:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, name=name)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


game = CRUDGame(Game)
