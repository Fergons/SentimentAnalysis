import asyncio
import logging

from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from typing import AsyncGenerator, List

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import config
from app.models import Base, Source, Review, Game
from app.schemas import SourceCreate, GameCreate, ReviewCreate, ReviewerCreate
from app import crud

from app.services.scraper.constants import SOURCES
from app.services.scraper.steam_resources import SteamAppDetail, SteamReview
from app.db.session import async_engine, async_session
from app.services.scraper.scraper import SteamScraper, GamespotScraper, DoupeScraper
from app.services.scraper.db_scraper import DBScraper
from app.models.source import GameSource

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger("test_db.py")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def steam_db_scraper(session: AsyncSession, sources):
    async with SteamScraper() as scraper:
        yield await DBScraper.create(scraper=scraper, session=session)


@pytest.fixture
async def gamespot_db_scraper(session: AsyncSession, sources):
    async with GamespotScraper(api_key=config.settings.GAMESPOT_API_KEY) as scraper:
        yield await DBScraper.create(scraper=scraper, session=session)


@pytest.fixture
async def doupe_db_scraper(session: AsyncSession, sources):
    async with DoupeScraper() as scraper:
        yield await DBScraper.create(scraper=scraper, session=session)


@pytest.fixture
async def sources(session: AsyncSession):
    """Create sources in db if not in db"""
    results = []
    for name, value in SOURCES.items():
        source = await crud.source.get_by_name(session, name=name)
        if source is None:
            source = await crud.source.create(session, obj_in=SourceCreate(**value))
        results.append(source)


@pytest.mark.anyio
async def test_create_db_sources(session: AsyncSession):
    results = []
    for name, value in SOURCES.items():
        new_source = await crud.source.create(session, obj_in=SourceCreate(**value))
        results.append(new_source)
    assert len(results) == len(SOURCES.keys())

    result = await session.execute(select(Source))
    assert len(result.scalars().all()) == len(SOURCES.keys())


@pytest.mark.anyio
async def test_create_db_games(session: AsyncSession):
    steam = await crud.source.get_by_name(session, name="steam")
    assert steam is not None

    async with SteamScraper() as scraper:
        result = await scraper.get_games_info([730, 1938090])
    assert len(result) == 2
    for detail in result:
        logger.log(logging.DEBUG, detail.dict(by_alias=True))
        detail_dict = detail.dict(by_alias=True)
        categories_names = [category.description for category in detail.categories]
        obj_in = GameCreate(source_id=steam.id, **detail_dict)
        logger.log(logging.DEBUG, obj_in.dict())
        game = await crud.game.create_with_categories_by_names_and_source(session,
                                                                          obj_in=obj_in,
                                                                          source_game_id=detail_dict.get(
                                                                              "source_game_id"),
                                                                          source_id=steam.id,
                                                                          names=categories_names)
        assert game.name == detail.name
        assert game.sources is not None
        assert game.sources[0].source_id == steam.id


# @pytest.mark.anyio
# async def test_create_db_reviews(session: AsyncSession):
#     games = await crud.game.get_multi(session)
#     assert len(games) == 2
#     source_id = games[0].sources[0].source_id
#     game_ids = [game.id for game in games]
#     source_game_ids = [game.sources[0].source_game_id for game in games]
#     async with steam_scraper as scraper:
#         results = await scraper.get_games_reviews(source_game_ids, [{"language": "czech", "limit": 100} for _ in range(len(source_game_ids))])
#         for game_id, db_game_id in zip(source_game_ids, game_ids):
#             reviews = results[game_id]
#             for review in reviews:
#                 review_db = await crud.review.create(session,
#                                                      obj_in=ReviewCreate.parse_obj(
#                                                          review.dict(by_alias=True, exclude={"author": True})))
#                 review_db.game_id = db_game_id
#                 review_db.source_id = games[0].sources[0].source_id
#                 await session.commit()
#                 await session.refresh(review_db)
#
#     result = await session.execute(select(Review))
#     assert len(result.scalars().all()) == 200


# @pytest.mark.anyio
# async def test_crud_review_create_multi(session: AsyncSession):
#     _max = 100
#     games = await crud.game.get_multi(session)
#     assert len(games) == 2
#     source_id = games[0].sources[0].source_id
#     game_ids = [game.id for game in games]
#     source_game_ids = [game.sources[0].source_game_id for game in games]
#     async with SteamScraper() as scraper:
#         results = await scraper.get_games_reviews(source_game_ids, [{"language": "czech", "limit": _max} for _ in range(len(source_game_ids))])
#         review_create_objs = [
#             ReviewCreate(source_id=source_id, game_id=db_game_id, **review.dict(by_alias=True))
#             for game_id, db_game_id in zip(source_game_ids, game_ids)
#             for review in results[game_id]
#         ]
#
#         await crud.review.create_multi(session, objs_in=review_create_objs)
#
#     result = await session.execute(select(Review))
#     reviews_in_db = result.scalars().all()
#     logger.log(logging.DEBUG, f"number of review in table: {len(reviews_in_db)}")
#     assert len(reviews_in_db) >= _max - int(_max / 2)


@pytest.mark.anyio
async def test_steam_db_scraper_scrape_games(steam_db_scraper, session: AsyncSession):
    num_of_games = 2
    scraped_games = await steam_db_scraper.scrape_games(bulk_size=20, end_after=num_of_games)
    result = await session.execute(
        select(GameSource.game_id).where(GameSource.source_id == steam_db_scraper.db_source.id))
    games_in_db = result.scalars().all()
    # check if scraped_games are in db
    assert all(map(lambda x: x in games_in_db, scraped_games))


# @pytest.mark.anyio
# async def test_steam_db_scraper_scrape_reviews(steam_db_scraper, session: AsyncSession):
#     await steam_db_scraper.scrape_all_reviews_for_not_updated_steam_games(max_reviews=100)
#     result = await session.execute(select(Review).where(Review.source_id == steam_db_scraper.db_source.id))
#     reviews_in_db = result.scalars().all()
#     assert all(map(lambda x: x.reviewer_id is not None, reviews_in_db))


# @pytest.mark.anyio
# async def test_gamespot_db_scraper(gamespot_db_scraper, session: AsyncSession):
#     result = await session.execute(select(Review).where(Review.source_id == gamespot_db_scraper.db_source.id))
#     reviews_in_db = result.scalars().all()
#     assert len(reviews_in_db) == 0
#     await gamespot_db_scraper.scrape_all_reviews(max_reviews=3)
#     result = await session.execute(select(Review).where(Review.source_id == gamespot_db_scraper.db_source.id))
#     reviews_in_db = result.scalars().all()
#     logger.debug(f"Num gamespot reviews in db: {len(reviews_in_db)}")
#     assert len(reviews_in_db) > 0


# @pytest.mark.anyio
# async def test_doupe_db_scraper(doupe_db_scraper, session: AsyncSession):
#     await doupe_db_scraper.scrape_all_reviews(max_reviews=100)
#     result = await session.execute(select(Review).where(Review.source_id == doupe_db_scraper.db_source.id))
#     reviews_in_db = result.scalars().all()
#     logger.debug(f"Num doupe reviews in db: {len(reviews_in_db)}")
#     assert len(reviews_in_db) > 0


# @pytest.mark.anyio
# async def test_get_steam_reviews_100_limit_100_offset(steam_db_scraper, session: AsyncSession):
#     reviews = await crud.review.get_not_processed_by_source(session,
#                                                             source_id=steam_db_scraper.db_source.id,
#                                                             limit=100,
#                                                             offset=100)
#     logger.debug(len(reviews))
#     assert len(reviews) <= 100
#     assert all(map(lambda x: x.processed_at is None, reviews))


@pytest.mark.anyio
async def test_scrape_reviews_for_game(steam_db_scraper, session: AsyncSession):
    game = await crud.game.get(session, 1)
    assert game is not None
    game_id, num_reviews = await steam_db_scraper.scrape_reviews_for_game(game_id=game.id, language="czech", max_reviews=300)
    result = await session.execute(select(Review.id).where(
        and_(Review.game_id == game.id, Review.source_id == steam_db_scraper.db_source.id)))
    num_reviews_in_db = len(result.scalars().all())
    assert num_reviews == num_reviews_in_db
