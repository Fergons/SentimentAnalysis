import asyncio
from sqlalchemy.future import select
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import config
from app.models import Base, Source
from app.schemas import SourceCreate
from app.crud import crud_source

from app.services.scraper.constants import SOURCES
from app.db.session import async_engine, async_session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def init_db():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine._url) == config.settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture
async def session(init_db) -> AsyncGenerator[AsyncSession, None]:
    async with init_db() as session:
        yield session


@pytest.fixture
async def test_create_db_sources(session: AsyncSession):
    results = []
    for name, value in SOURCES.items():
        new_source = await crud_source.create(session, obj_in=SourceCreate(**value))
        results.append(new_source)
    assert len(results) == 3

    result = await session.execute(select(Source))
    assert len(result.scalars().all()) == 3