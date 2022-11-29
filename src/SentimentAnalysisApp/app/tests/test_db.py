import asyncio
import logging

from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from typing import AsyncGenerator, List

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import config
from app.models import Base, Source, Review
from app.schemas import SourceCreate, GameFromSourceCreate, ReviewCreate, ReviewerCreate
from app.crud import crud_source, crud_game, crud_review

from app.services.scraper.constants import SOURCES
from app.services.scraper.steam_resources import SteamAppDetail, SteamReview
from app.db.session import async_engine, async_session
from app.services.scraper.scraper import SteamScraper
from app.models.source import GameSource

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger("test_db.py")
steam_scraper = SteamScraper()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def init_db():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == config.settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture
async def session(init_db) -> AsyncGenerator[AsyncSession, None]:
    async with init_db() as session:
        try:
            yield session
        except:
            logger.log(logging.CRITICAL, f"Integrity error calling session.close()")
        finally:
            session.close()


@pytest.mark.anyio
async def test_create_db_sources(session: AsyncSession):
    results = []
    for name, value in SOURCES.items():
        new_source = await crud_source.create(session, obj_in=SourceCreate(**value))
        results.append(new_source)
    assert len(results) == 3

    result = await session.execute(select(Source))
    assert len(result.scalars().all()) == 3


@pytest.mark.anyio
async def test_create_db_games(session: AsyncSession):
    steam = await crud_source.get_by_name(session, name="steam")
    assert steam is not None

    async with steam_scraper as scraper:
        result = await scraper.get_games_info([730, 630])
    assert len(result) == 2
    for detail in result:
        logger.log(logging.DEBUG, detail.dict(by_alias=True))
        detail_dict = detail.dict(by_alias=True)
        categories_names = [category.description for category in detail.categories]
        obj_in = GameFromSourceCreate(source_id=steam.id, **detail_dict)
        logger.log(logging.DEBUG, obj_in.dict())
        game = await crud_game.create_with_categories_by_names_and_source(session, obj_in=obj_in, names=categories_names)
        assert game.name == detail.name
        assert game.sources is not None
        assert game.sources[0].source_id == steam.id


@pytest.mark.anyio
async def test_create_db_reviews(session: AsyncSession):
    games = await crud_game.get_multi(session)
    assert len(games) == 2
    source_id = games[0].sources[0].source_id
    game_ids = [game.id for game in games]
    source_game_ids = [game.sources[0].source_game_id for game in games]
    async with steam_scraper as scraper:
        results = await scraper.get_games_reviews(source_game_ids, [{"language": "czech", "limit": 100} for _ in range(len(source_game_ids))])
        for game_id, db_game_id in zip(source_game_ids, game_ids):
            reviews = results[game_id]
            for review in reviews:
                review_db = await crud_review.create(session,
                                                     obj_in=ReviewCreate.parse_obj(
                                                         review.dict(by_alias=True, exclude={"author": True})))
                review_db.game_id = db_game_id
                review_db.source_id = games[0].sources[0].source_id
                await session.commit()
                await session.refresh(review_db)

    result = await session.execute(select(Review))
    assert len(result.scalars().all()) == 200


@pytest.mark.anyio
async def test_crud_review_create_multi(session: AsyncSession):
    _max = 1000
    games = await crud_game.get_multi(session)
    assert len(games) == 2
    source_id = games[0].sources[0].source_id
    game_ids = [game.id for game in games]
    source_game_ids = [game.sources[0].source_game_id for game in games]
    async with steam_scraper as scraper:
        results = await scraper.get_games_reviews(source_game_ids, [{"language": "czech", "limit": _max} for _ in range(len(source_game_ids))])
        review_create_objs = [
            ReviewCreate(source_id=source_id, game_id=db_game_id, **review.dict(by_alias=True))
            for game_id, db_game_id in zip(source_game_ids, game_ids)
            for review in results[game_id]
        ]

        await crud_review.create_multi(session, objs_in=review_create_objs)

    result = await session.execute(select(Review))
    reviews_in_db = result.scalars().all()
    logger.log(logging.DEBUG, f"number of review in table: {len(reviews_in_db)}")
    assert len(reviews_in_db) >= _max - int(_max / 2)

@pytest.mark.anyio
async def test_crud_review_create_review_with_reviewer(session: AsyncSession):
    games = await crud_game.get_multi(session)
    assert len(games) == 2
    source_id = games[0].sources[0].source_id
    game_ids = [game.id for game in games]
    source_game_ids = [game.sources[0].source_game_id for game in games]
    async with steam_scraper as scraper:
        results = await scraper.get_games_reviews(source_game_ids, [{"language": "czech", "limit": 100} for _ in range(len(source_game_ids))])
        review_create_objs = [
            ReviewCreate.parse_obj({"source_id": source_id, "game_id": db_game_id, **review.dict(by_alias=True)})
            for game_id, db_game_id in zip(source_game_ids, game_ids)
            for review in results[game_id]
        ]
        logger.log(logging.DEBUG, review_create_objs[0].reviewer)
        await crud_review.create_with_reviewer_multi(session, objs_in=review_create_objs)

    result = await session.execute(select(Review))
    reviews_in_db = result.scalars().all()
    logger.log(logging.DEBUG, f"number of review in table: {len(reviews_in_db)}")
    assert len(reviews_in_db) >= 150

@pytest.mark.anyio
async def test_remove_game(session: AsyncSession):
    games = await crud_game.get_multi(session)
    assert len(games) == 2
    await crud_game.remove(session, id=games[1].id)
    games = await crud_game.get_multi(session)
    assert len(games) == 1
    result = await session.execute(select(GameSource))
    #test cascade delete
    gamesources = result.scalars().all()
    assert len(gamesources) == 1
