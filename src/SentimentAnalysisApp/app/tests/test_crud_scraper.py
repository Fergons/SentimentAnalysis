from datetime import datetime
import random

import pytest
import httpx
import respx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from sqlalchemy.orm import selectinload

from app.services.scraper.steam_resources import SteamAppDetail, SteamReview, SteamAppListResponse, SteamApp, \
    SteamAppReviewsResponse, SteamMetacriticReview, SteamAppCategory
from app import crud, schemas, models
import asyncio
from .test_data import TEST_SOURCE

pytestmark = pytest.mark.anyio

steam_applist_response = {
    "applist": {"apps": [
        {"appid": 730, "name": "Counter-Strike: Global Offensive"},
        {"appid": 440, "name": "Team Fortress 2"},
        {"appid": 570, "name": "Dota 2"},
        {"appid": 4000, "name": "Garry's Mod"},
        {"appid": 550, "name": "Left 4 Dead 2"},
        {"appid": 620, "name": "Portal 2"},
        {"appid": 80, "name": "Counter-Strike: Condition Zero"}]
    }
}


def generate_n_scraped_reviews(
        n: int, source_id: int, appid: Optional[int] = None, reviewer_id: Optional[int] = None
) -> List[schemas.ScrapedReview]:
    # create a list of n scraped reviews with unique data
    scraped_reviews = []

    for i in range(n):
        _appid = appid or random.randint(0, 120)
        _reviewer_id = reviewer_id or random.randint(0, 100)
        scraped_review = schemas.ScrapedReview(
            text=f"Test Review {i}",
            language="english",
            reviewer=schemas.ScrapedReviewer(
                name=f"Test Reviewer {_reviewer_id}",
                source_id=source_id,
                source_reviewer_id=f"test_reviewer_id_{_reviewer_id}",
                num_games_owned=100,
                num_reviews=100
            ),
            game=schemas.ScrapedGame(
                name=f"Test Game {_appid}",
                source_id=source_id,
                source_game_id=f"test_appid_{_appid}",
                categories=[f"Test Category {random.randint(0, 20)}", f"Test Category {random.randint(0, 10)}"],
                developers=[f"Test Developer {random.randint(0, 10)}", f"Test Developer {random.randint(0, 10)}"]
            ),
            source_id=source_id,
            source_review_id=f"test_review_id_{i}_appid_{_appid}",
            summary=f"Test Summary {i}",
            score=f"Test Score {i}",
            helpful_score=f"Test Helpful Score {i}",
            good=f"Test Good {i}",
            bad=f"Test Bad {i}",
            voted_up=True,
            playtime_at_review=100,
            created_at=datetime.now()
        )
        scraped_reviews.append(scraped_review)
    return scraped_reviews


def mock_steam_app_detail(appid=730, name="Counter-Strike: Global Offensive") -> SteamAppDetail:
    app_detail = SteamAppDetail(
        type="game",
        name=name,
        steam_appid=appid,
        supported_languages="English,Czech",
        header_image=f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg?t=1617720000",
        developers=["Valve", f"Dev{appid}"],
        publishers=["Valve"],
        metacritic=SteamMetacriticReview(score=88, url="https://www.metacritic.com/game/pc/team-fortress-2"),
        categories=[{"id": 1, "description": "Action"}, {"id": 2, "description": "FPS"}],
        release_date={"coming_soon": False, "date": "10 Oct, 2007"}
    )
    return app_detail


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def source(session: AsyncSession):
    source_in = schemas.SourceCreate(name="test_source", url="https://test_source.com")
    source = await crud.source.get_by_name(session, name=source_in.name)
    if not source:
        source = await crud.source.create(session, obj_in=source_in)
    return source


@pytest.fixture
async def game(session: AsyncSession):
    game = models.Game(id=999,
                       name="test_game",
                       image_url="https://test_game.com",
                       release_date=datetime(2021, 1, 1))
    session.add(game)
    await session.commit()
    return game


async def test_store_game(clear_db, session: AsyncSession, source: models.Source):
    scraped_game_data = {
        "name": "Test Game",
        "source_id": source.id,
        "source_game_id": "test_game_id",
    }

    scraped_game = schemas.ScrapedGame(**scraped_game_data)
    game = await crud.scraper.store_game(session, scraped_obj=scraped_game)
    source = await session.execute(
        select(models.Source).where(models.Source.id == source.id).options(selectinload('*')))
    source = source.scalars().first()
    game = await session.execute(select(models.Game).where(models.Game.id == game.id).options(selectinload('*')))
    game = game.scalars().first()

    assert game.id is not None
    assert game.name == scraped_game_data["name"]
    assert game.sources[0].source_id == source.id
    assert game.sources[0].source_game_id == scraped_game_data["source_game_id"]


async def test_store_game_with_additional_objects(clear_db, session: AsyncSession, source: models.Source, ):
    # Replace with actual scraped game data
    scraped_game_data = {
        "name": "Test Game 2",
        "source_id": source.id,
        "source_game_id": "test_game_id_2",
        "categories": ["Test Category"],
        "developers": ["Test Developer", "Test Developer 2"],
    }
    scraped_game = schemas.ScrapedGame(**scraped_game_data)
    game = await crud.scraper.store_game_with_additional_objects(session, scraped_obj=scraped_game)
    source = await session.execute(
        select(models.Source).where(models.Source.id == source.id).options(selectinload(models.Source.games)))
    source = source.scalars().first()
    game = await session.execute(select(models.Game).where(models.Game.id == game.id).options(selectinload('*')))
    game = game.scalars().first()
    assert game.id is not None
    assert game.name == scraped_game_data["name"]
    assert len(game.sources) == 1
    assert game.sources[0].source_id == source.id
    assert game.sources[0].source_game_id == scraped_game_data["source_game_id"]
    assert len(game.categories) == 1
    assert game.categories[0].category.name == scraped_game_data["categories"][0]
    assert len(game.developers) == 2
    assert game.developers[0].developer.name == scraped_game_data["developers"][0]
    assert game.developers[1].developer.name == scraped_game_data["developers"][1]
    assert len(source.games) == 1


async def test_store_game_with_additional_objects_race_conditions(clear_db, session: AsyncSession,
                                                                  get_session_maker: AsyncSession,
                                                                  source: models.Source):
    async def create_game(task_name: str, task_id: int, game_id: Optional[int] = None):
        scraped_game = schemas.ScrapedGame(
            name=f"Test Game {task_name} task_id_{task_id} game_id_{game_id}",
            source_id=source.id,
            source_game_id=f"test_game_id_{game_id}" if game_id else f"test_task_id_{task_id}",
            categories=[f"Test Category task_id {task_id}", "Default Category", "Default Category 2"],
            developers=[f"Test Developer task_id {task_id}", "Default Developer", "Default Developer 2"]
        )
        async with get_session_maker() as oob_session:
            await crud.scraper.store_game_with_additional_objects(oob_session, scraped_obj=scraped_game)

    # Create the same game in parallel to test race condition
    tasks = [asyncio.create_task(create_game("Same Game", task_id, game_id=1)) for task_id in range(5)]
    await asyncio.gather(*tasks)
    # Check if only one game with the same name exists in the database
    games = await session.execute(select(models.Game))
    games = games.scalars().all()
    assert len(games) == 1

    # Create unique games with the same developer or category
    tasks = [asyncio.create_task(create_game("Unique Game", task_id)) for task_id in range(5)]
    await asyncio.gather(*tasks)

    # Check if more than one game exists in the database
    games = await session.execute(select(models.Game))
    games = games.scalars().all()
    assert len(games) > 1


async def test_store_review(clear_db, session: AsyncSession, source: models.Source, game: models.Game):
    """
    Test crud scraper store review in db
    """
    scraped_review = schemas.ScrapedReview(
        text="Test Review",
        language="english",
        reviewer=schemas.ScrapedReviewer(
            name="Test Reviewer",
            source_id=source.id,
            source_reviewer_id="test_reviewer_id",
            num_games_owned=100,
            num_reviews=100
        ),
        game=schemas.ScrapedGame(
            name="Test Game",
            source_id=source.id,
            source_game_id="test_game_id",
            categories=["Test Category"],
            developers=["Test Developer", "Test Developer 2"]
        ),
        game_id=game.id,
        source_id=source.id,
        source_review_id="test_review_id",
        summary="Test Summary",
        score="Test Score",
        helpful_score="Test Helpful Score",
        good="Test Good",
        bad="Test Bad",
        voted_up=True,
        playtime_at_review=100,
        created_at=datetime.now()
    )
    await crud.source.add_game(session, game_id=game.id, source_id=source.id,
                               source_game_id=f"game_{game.id}_source_{source.id}")
    review = await crud.scraper.store_review(session, scraped_obj=scraped_review)
    review = await session.execute(
        select(models.Review).where(models.Review.id == review.id).options(selectinload('*')))
    review = review.scalars().first()

    assert review.id is not None
    assert review.source_id == source.id
    assert review.source_review_id == scraped_review.source_review_id

    assert review.game == game
    assert review.source == source


async def test_store_review_with_additional_objects(clear_db, session: AsyncSession, source: models.Source):
    """
    Test crud scraper store review in db
    """
    scraped_review = schemas.ScrapedReview(
        text="Test Review",
        language="english",
        reviewer=schemas.ScrapedReviewer(
            name="Test Reviewer",
            source_id=source.id,
            source_reviewer_id="test_reviewer_id",
            num_games_owned=100,
            num_reviews=100
        ),
        game=schemas.ScrapedGame(
            name="Test Game",
            source_id=source.id,
            source_game_id="test_game_id",
            categories=["Test Category"],
            developers=["Test Developer", "Test Developer 2"]
        ),
        source_id=source.id,
        source_review_id="test_review_id",
        summary="Test Summary",
        score="Test Score",
        helpful_score="Test Helpful Score",
        good="Test Good",
        bad="Test Bad",
        voted_up=True,
        playtime_at_review=100,
        created_at=datetime.now()
    )
    review = await crud.scraper.store_review_with_additional_objects(session, scraped_obj=scraped_review)
    review = await session.execute(
        select(models.Review).where(models.Review.id == review.id).options(selectinload('*')))
    review = review.scalars().first()

    assert review.id is not None
    assert review.source_id == source.id
    assert review.source_review_id == scraped_review.source_review_id

    assert review.game is not None
    assert review.game.name == scraped_review.game.name
    assert review.source.id == source.id

    reviewer = await session.execute(select(models.Reviewer).where(models.Reviewer.id == review.reviewer_id))
    reviewer = reviewer.scalars().first()
    assert reviewer is not None
    assert reviewer.name == scraped_review.reviewer.name


async def test_store_review_with_additional_objects_on_many_reviews(clear_db, source: models.Source, get_session_maker: AsyncSession):
    """
    Generates many reviews and stores them in the database
    """

    scraped_reviews = generate_n_scraped_reviews(1000, source_id=source.id)
    scraped_reviews2 = generate_n_scraped_reviews(100, source_id=source.id, appid=730)

    async def save_multiple_reviews(reviews):
        async with get_session_maker() as oob_session:
            for review in reviews:
                await crud.scraper.store_review_with_additional_objects(oob_session, scraped_obj=review)

    tasks = []
    for r in [scraped_reviews, scraped_reviews2]:
        tasks.append(asyncio.create_task(save_multiple_reviews(r)))

    await asyncio.gather(*tasks)

    async with get_session_maker() as session:
        reviews = await session.execute(select(models.Review))
        reviews = reviews.scalars().all()
    assert len(reviews) == len(scraped_reviews) + len(scraped_reviews2)
