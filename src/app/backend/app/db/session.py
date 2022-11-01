import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.app.core.config import settings

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
