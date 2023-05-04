import os
import pytest
import logging
from ..scraper import GamespotScraper
from ..gamespot_resources import (GamespotRequestParams,
                                  GamespotSortParam,
                                  GamespotReviewsSortFields,
                                  SortDirection)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def scraper():
    Meta = GamespotScraper
    return Meta(api_key=os.environ.get("GAMESPOT_API_KEY"))


@pytest.mark.anyio
async def test_get_games_reviews_gamespot(scraper):
    assert os.environ.get("GAMESPOT_API_KEY") is not None
    assert scraper.api_key is not None

    reviews = []
    async with scraper as scraper:
        async for page in scraper.game_reviews_page_generator(max_reviews=100):
            reviews.extend(page)
