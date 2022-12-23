import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserDB
from app import models
import logging
from .utils import create_objs
from .test_data import (TEST_CATEGORY,
                        TEST_GAME,
                        TEST_GAME_CATEGORY,
                        TEST_GAME_SOURCE,
                        TEST_REVIEW,
                        TEST_REVIEWER,
                        TEST_SOURCE)

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.anyio
logger = logging.getLogger()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def seed_initial_test_data(session: AsyncSession):
    # seed table category
    categories = await create_objs(session, models.Category, TEST_CATEGORY)
    # seed table source
    sources = await create_objs(session, models.Source, TEST_SOURCE)
    # seed table game
    games = await create_objs(session, models.Game, TEST_GAME)
    # seed table game_source
    game_sources = await create_objs(session, models.GameSource, TEST_GAME_SOURCE)
    # seed table game_category
    game_categories = await create_objs(session, models.GameCategory, TEST_GAME_CATEGORY)
    # seed table reviewer
    reviewers = await create_objs(session, models.Reviewer, TEST_REVIEWER)
    # seed table review
    reviews = await create_objs(session, models.Review, TEST_REVIEW)

    return {"category": categories,
            "source": sources,
            "game": games,
            "gamesource": game_sources,
            "gamecategory": game_categories,
            "reviewer": reviewers,
            "review": reviews
            }


async def test_get_games_endpoint(client: AsyncClient, default_user: UserDB, access_token: str, seed_initial_test_data):
    # test get games endpoint
    resp = await client.get(
        "/games/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    logger.info(data)
