from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import update
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import load_only

from app.db.base import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalars().first()
        return obj

    async def get_by_source_id(self, db: AsyncSession, source_id: Any, source_obj_id: Any) -> Optional[ModelType]:
        result = await db.scalars(
            select(self.model)
            .where(
                (self.model.source_id == source_id) &
                (getattr(self.model, f"source_{self.model.__tablename__}_id") == source_obj_id)
            )
        )
        return result.first()

    async def get_id_by_source_id(self, db: AsyncSession, source_id: Any, source_obj_id: Any) -> Optional[int]:
        result = await db.scalars(
            select(self.model.id)
            .where(
                (self.model.source_id == source_id) &
                (getattr(self.model, f"source_{self.model.__tablename__}_id") == source_obj_id)
            )
        )
        return result.first()

    async def get_multi(
            self, db: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = await db.scalars(select(self.model).offset(offset).limit(limit))
        return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())  # type: ignore
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = inspect(db_obj).attrs.keys()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalars().first()
        await db.delete(obj)
        await db.commit()
        return obj

    async def touch(self, db: AsyncSession, *, obj_id: int):
        await db.execute(update(self.model).where(self.model.id == obj_id))

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.name == name))
        return result.scalars().first()

    async def create_multi_by_names(self, db: AsyncSession, *, names: List[str]) -> List[ModelType]:
        # check if in db already
        db_objs = []
        for name in names:
            db_obj = await self.get_by_name(db, name=name)
            if db_obj is None:
                db_obj = self.model(name=name)
                db.add(db_obj)
            db_objs.append(db_obj)
        await db.commit()
        return db_objs

    async def create_multi(self, db: AsyncSession, *, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        db_objs = [self.model(**obj.dict()) for obj in objs_in]
        db.add_all(db_objs)
        await db.commit()
        return db_objs

    async def update_multi(self, db: AsyncSession, *, db_objs: ModelType, objs_in: List[UpdateSchemaType]
                           ) -> List[ModelType]:
        for db_obj, obj_in in zip(db_objs, objs_in):
            obj_data = inspect(db_obj).attrs.keys()
            update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
        db.add_all(db_objs)
        await db.commit()
        return db_objs
