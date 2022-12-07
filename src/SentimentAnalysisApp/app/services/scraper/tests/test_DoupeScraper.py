import pytest
from ..scraper import DoupeScraper


@pytest.mark.asyncio
async def test_get_game_reviews(logger):
    reviews = []
    async with DoupeScraper() as scraper:
        async for page in scraper.game_reviews_page_generator():
            reviews.extend(page)

    logger.debug(reviews)
    logger.debug(f"Number of reviews fetched: {len(reviews)}")

    assert len(reviews) > 0
