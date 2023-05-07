"""
Created by Frantisek Sabol
Tests for the SteamScraper class.
"""
import hashlib
import json
from ..scraper import SteamScraper
import pytest


import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger()


@pytest.mark.anyio
async def test_get_games_info():
    async with SteamScraper() as scraper:
        infos = await scraper.get_games_info([730, 630])
    assert len(infos) == 2



@pytest.mark.anyio
async def test_get_game_reviews():
    reviews = []
    async with SteamScraper() as scraper:
        async for page in scraper.game_reviews_page_generator(730, max_reviews=200):
            reviews.extend(page)
    assert len(reviews) > 100


# possible errors due to unexpected returns and blocking rate limits
@pytest.mark.anyio
async def test_get_game_reviews_with_large_limit():
    reviews = []
    max_reviews = 200
    async with SteamScraper() as scraper:
        async for page in scraper.game_reviews_page_generator(730, language="czech", max_reviews=max_reviews):

            try:
                assert all(map(lambda x: x.language == "czech", page))
            except AssertionError:
                # ??? random language assigned to the review but text seems to be czech everytime
                logger.log(logging.ERROR, f"api call ({scraper.request_counter - 1}): {list(map(lambda x: x.get('language'), page))}")

            reviews.extend(page)

    assert len(reviews) > 0
    assert len(reviews) <= max_reviews


@pytest.mark.anyio
async def test_get_reviews_from_list_of_game_ids():
    async with SteamScraper() as scraper:
        await scraper.get_games_reviews([730, 620, 578080], [{"language": "czech", "max_reviews": 1000} for x in range(3)])







