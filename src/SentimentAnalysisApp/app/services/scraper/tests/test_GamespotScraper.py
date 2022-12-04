import os
from typing import AsyncGenerator

import pytest
import logging
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core import config
from db.base_class import Base
from db.session import async_engine, async_session

from app.models.review import Review
from ..scrape_to_db import DBScraper
from ..scraper import GamespotScraper
from ..gamespot_resources import (GamespotRequestParams,
                                  GamespotSortParam,
                                  GamespotReviewsSortFields,
                                  SortDirection)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == config.settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        yield session

# @pytest.fixture
# def scraper():
#     Meta = GamespotScraper
#     return Meta()
#
#
# @pytest.fixture
# async def db_scraper(scraper: GamespotScraper, session: AsyncSession) -> DBScraper:
#     async with scraper as scraper:
#         yield await DBScraper.create(scraper=scraper, session=session)


# @pytest.mark.anyio
# async def test_get_games_reviews_gamespot(scraper):
#     assert os.environ.get("GAMESPOT_API_KEY") is not None
#     assert scraper._api_key is not None
#
#     reviews = []
#     async with scraper as scraper:
#         async for page in scraper.game_reviews_page_generator(max_reviews=500):
#             reviews.extend(page)


@pytest.mark.anyio
async def test_scrape_gamespot_reviews_to_db(session: AsyncSession):
    async with GamespotScraper() as scraper:

        db_scraper = await DBScraper.create(scraper=scraper, session=session)
        logger.debug(db_scraper.db_source.id)
        await db_scraper.scrape_all_reviews_with_game()
    result = await session.execute(select(Review))
    reviews = result.scalars().all()
    logger.info(f"{len(reviews)} are in the db!")
    assert len(reviews) > 0