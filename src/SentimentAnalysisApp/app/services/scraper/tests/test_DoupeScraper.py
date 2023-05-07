"""
Created by Frantisek Sabol
Tests for DoupeScraper
"""
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


@pytest.mark.asyncio
async def test_get_game_reviews_with_detail(logger):
    reviews = []
    async with DoupeScraper() as scraper:
        async for page in scraper.game_reviews_page_generator(max_pages=2):
            results = await scraper.get_reviews_detail(reviews=page)
            logger.debug(results)
            reviews.extend(results)

    logger.debug(reviews)
    logger.debug(f"Number of reviews fetched: {len(reviews)}")

    assert len(reviews) > 0