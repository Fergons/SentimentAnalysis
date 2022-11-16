from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.game import Game, Category
from app.schemas.game import GameCreate, GameUpdate
from app.schemas.game import CategoryCreate, CategoryUpdate, CategoryBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        result = await db.execute(select(Category).where(Category.name == name))
        return result.scalars().first()


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    async def create_with_categories_by_names(
            self, db: AsyncSession, *, obj_in: GameCreate, categories_by_names: List[str]
    ) -> Game:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        for name in categories_by_names:
            new_c = await crud_category.get_by_name(db, name=name)
            if new_c is None:
                new_c = await crud_category.create(db, obj_in=CategoryCreate(name=name))
            if new_c is not None:
                db_obj.categories.append(new_c)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_game = CRUDGame(Game)
crud_category = CRUDCategory(Category)
