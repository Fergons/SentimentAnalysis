from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.core.config import settings
from backend.app.db import base  # noqa: F401
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL")
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        user = crud.user.get_by_name(db, name=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                name="admin"
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841

