import argparse
import asyncio
import logging
import random
from typing import List, Optional, Union, TypeVar, Tuple

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.crud.source import crud_source
from app.crud.review import crud_review
from app.schemas.game import GameCreate
from app.crud.game import crud_game
from app.schemas.review import ReviewCreate, ReviewCreate
from app.schemas.source import GameSourceCreate
from app.schemas.reviewer import ReviewerCreate
from app.crud.reviewer import crud_reviewer
from .scraper import SteamScraper, Scraper, DoupeScraper, GamespotScraper
from .gamespot_resources import GamespotRequestParams, GamespotReview, GamespotGame, GamespotReviewer
from .doupe_resources import DoupeReview, DoupeGame, DoupeReviewer
from .steam_resources import SteamAppListResponse, SteamApp, SteamReview, SteamAppDetail, SteamReviewer
from .constants import STEAM_REVIEWS_API_RATE_LIMIT, ScrapingResourceType
from app.core.config import settings
from sqlalchemy import exc

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger("scraper_to_db.py")

ScrapedReview = TypeVar('ScrapedReview', SteamReview, DoupeReview, GamespotReview)
ScrapedGame = TypeVar('ScrapedGame', SteamAppDetail, DoupeGame, GamespotGame)
ScrapedReviewer = TypeVar('ScrapedReviewer', SteamReviewer, DoupeReviewer, GamespotReviewer)

class DBScraper:
    @classmethod
    async def create(cls, scraper: Scraper, session: AsyncSession):
        self = DBScraper()
        self.scraper = scraper
        self.session = session
        self.db_source = await crud_source.get_by_url(self.session, url=self.scraper.url)
        if self.db_source is None:
            raise ValueError(f"Source {self.scraper.url} was not found in db!")
        return self

    def __init__(self):
        self.scraper = None
        self.session = None
        self.db_source = None

    async def scrape_games(self, bulk_size: int = 20, end_after: int = 1000) -> List[int]:
        db_game_ids = await crud_game.get_all_app_ids_from_source(self.session, source_id=self.db_source.id)
        games_scraped = []

        games: List[SteamApp] = await self.scraper.get_games()
        random.shuffle(games)

        logger.log(logging.INFO, f"{len(db_game_ids)}/{len(games)} already in db!")
        group_counter = 1
        for bulk_start in range(0, len(games), bulk_size):
            tasks = []
            for game in games[bulk_start:bulk_start + bulk_size]:
                if str(game.appid) in db_game_ids:
                    continue
                tasks.append(self.scraper.get_game_info(game.appid))

            counter = 0
            for future in asyncio.as_completed(tasks):
                counter += 1
                detail: Optional[SteamAppDetail] = await future

                if detail is None:
                    continue
                logger.log(logging.DEBUG, f"{type(detail)}: {detail}")

                db_game = await crud_game.get_by_source_id(
                    self.session, source_id=self.db_source.id, source_game_id=detail.steam_appid)
                logger.debug(
                    f"App {detail.steam_appid} checked if in db: {db_game.id if db_game is not None else 'Not found'}")
                if db_game is not None:
                    continue

                if detail.type != "game":
                    try:
                        logger.debug("Creating non-game app...")
                        await crud_game.create_non_game_app_from_source(
                            self.session, source_id=self.db_source.id, source_obj_id=detail.steam_appid
                        )
                    except exc.IntegrityError as e:
                        logger.error(f"Integrity Error: {e}")
                    finally:
                        continue

                obj_in = GameCreate(
                    **detail.dict(by_alias=True)
                )
                categories = [category.description for category in detail.categories]
                categories.extend([genre.description for genre in detail.genres])
                logger.debug(f"Creating game {detail.steam_appid} with categories: {categories}")
                game = await crud_game.create_with_categories_by_names_and_source(
                    self.session, obj_in=obj_in, source_id=self.db_source.id, source_game_id=detail.steam_appid,
                    names=categories
                )
                logger.debug(f"Game {detail.steam_appid} created!")
                games_scraped.append(game.id)
                if len(games_scraped) >= end_after:
                    logger.info(f"Scraped {len(games_scraped)} games, ending...")
                    return games_scraped

                logger.log(logging.INFO, f"Progress {counter}/{len(tasks)} tasks done!")

            logger.log(logging.INFO, f"Group {group_counter}/{len(games) // bulk_size} done!")
            group_counter += 1



    async def prepare_scraped_data(self, scraping: ScrapingResourceType,  **kwargs):
        if scraping == ScrapingResourceType.GAME:
            return self.prepare_game_data(data)
        elif scraping == ScrapingResourceType.REVIEW:
            return self.prepare_review_data(data)
        elif scraping == ScrapingResourceType.REVIEWER:
            return self.prepare_reviewer_data(data)
        else:
            raise ValueError(f"Unknown scraping resource type: {scraping}")

    def prepare_game_data(self, game: BaseModel) -> GameCreate:
        return GameCreate(
            **game.dict(by_alias=True)
        )

    def prepare_review_data(self, review: ScrapedReview) -> ReviewCreate:
        data = review.dict(by_alias=True)
        reviewer = data.get("reviewer_id")

        return ReviewCreate(
            **review.dict(by_alias=True)
        )

    def prepare_reviewer_data(self, reviewer: BaseModel) -> ReviewerCreate:
        return ReviewerCreate(
            **reviewer.dict(by_alias=True)
        )


    def apply_bulk_insert(cls, reviews: List[ScrapedReview], reviewers: List[ReviewerCreate]):
        return cls.insert_bulk_reviews_to_db

    async def insert_bulk_reviews_to_db(self, reviews: List[ScrapedReview], reviewers: List[ReviewerCreate]):

        for review in reviews:
            review.source_id = self.db_source.id

        await crud_reviewer.create_multi(self.session, reviewers)
        await crud_review.create_multi(self.session, reviews)

    async def scrape_all_reviews_for_not_updated_steam_games(self, game_ids: List[str] = None,
                                                             max_reviews: int = 100000):
        if game_ids is None:
            games = await crud_game.get_all_not_updated_db_games_from_source(self.session, source_id=self.db_source.id)
            game_ids = {game[1]: game[0] for game in games}

        # split game_ids into list containing lists of 10 game_ids
        _ids = list(game_ids.keys())
        bulks = [_ids[i:i + 10] for i in range(0, len(_ids), 10)]
        for bulk in bulks:
            tasks = [self.scraper.get_game_reviews(source_game_id)
                     for source_game_id in bulk]
            counter = 1
            for future in asyncio.as_completed(tasks):
                result = await future
                game_id, reviews = result

                if len(reviews) > 0:
                    review_create_objs = []
                    for review in reviews:
                        review_obj = ReviewCreate(source_id=self.db_source.id,
                                                  game_id=game_ids[game_id],
                                                  **review.dict(by_alias=True))
                        reviewer_obj = ReviewerCreate(source_id=self.db_source.id,
                                                      **review.author.dict(by_alias=True))

                        logger.debug(f"Checking if reviewer {reviewer_obj.source_reviewer_id} in db.")
                        db_reviewer_id = await crud_reviewer.get_id_by_source_id(self.session,
                                                                                 source_id=self.db_source.id,
                                                                                 source_obj_id=reviewer_obj.source_reviewer_id)
                        logger.debug(f"Reviewer {reviewer_obj.source_reviewer_id} in db: "
                                     f"{'FOUND' if db_reviewer_id is not None else 'NOT FOUND'}")
                        if db_reviewer_id is None:
                            db_reviewer = await crud_reviewer.create_from_source(self.session, obj_in=reviewer_obj)
                            db_reviewer_id = db_reviewer.id

                        review_obj.reviewer_id = db_reviewer_id
                        review_create_objs.append(review_obj)

                    logger.debug(f"Creating {len(review_create_objs)} reviews for game {game_id}...")
                    await crud_review.create_multi(self.session, objs_in=review_create_objs)
                    logger.debug(f"Created {len(review_create_objs)} reviews for game {game_id}!")

                logger.log(logging.INFO, f"{counter}. results are from: {game_id} num_reviews: {len(reviews)}!")
                logger.log(logging.INFO, f"Progress {counter}/{len(tasks)} tasks done!")
                counter += 1

    async def scrape_all_reviews(self, max_reviews: int = 100):
        async for page in self.scraper.game_reviews_page_generator(max_reviews=max_reviews):
            objs_in = []

            for review in page:
                review_data = review.dict(by_alias=True)
                review_obj = ReviewCreate.parse_obj(review_data)
                review_obj.source_id = self.db_source.id

                if review_data.get("game") is not None:
                    game_data = review.game.dict(by_alias=True)
                    source_game_id = game_data.get("source_game_id")
                    game_obj = GameCreate.parse_obj(game_data)
                    db_game = await crud_game.get_by_source_id(self.session,
                                                               source_id=self.db_source.id,
                                                               source_game_id=source_game_id)

                    if db_game is None:
                        db_game = await crud_game.create_from_source(self.session,
                                                                     obj_in=game_obj,
                                                                     source_id=self.db_source.id,
                                                                     source_game_id=source_game_id)
                    review_obj.game_id = db_game.id

                if review_data.get("reviewer") is not None:
                    reviewer_data = review.reviewer.dict(by_alias=True)
                    review_obj.playtime_at_review = reviewer_data.get("playtime_at_review")

                    reviewer_obj = ReviewerCreate.parse_obj(reviewer_data)
                    reviewer_obj.source_id = self.db_source.id

                    db_reviewer = await crud_reviewer.get_by_source_id(self.session,
                                                                       source_id=self.db_source.id,
                                                                       source_obj_id=reviewer_obj.source_reviewer_id)
                    if db_reviewer is None:
                        db_reviewer = await crud_reviewer.create_from_source(obj_in=reviewer_obj)
                    reviewer_obj.id = db_reviewer.id

                objs_in.append(review_obj)
                if len(objs_in) >= max_reviews:
                    break
            await crud_review.create_multi(self.session, objs_in=objs_in)


async def scrape_gamespot_reviews(rate_limit: dict = None):
    """Scrape gamespot reviews. This method is used to get initial data for system"""
    async with async_session() as session:
        async with GamespotScraper(api_key=settings.GAMESPOT_API_KEY, rate_limit=rate_limit) as scraper:
            db_scraper = await DBScraper.create(scraper, session)
            await db_scraper.scrape_all_reviews()


async def scrape_doupe_reviews(rate_limit: dict = None):
    """Scrape all reviews from doupe.cz. This method is used to get initial data for system"""
    async with async_session() as session:
        async with DoupeScraper(rate_limit=rate_limit) as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_all_reviews(max_reviews=2000)


async def scrape_steam_games(rate_limit: dict = None):
    """Scrape all games from steam. This method is used to get initial data for system"""
    async with async_session() as session:
        async with SteamScraper(rate_limit={"max_rate": 2, "time_period": 3}) as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_games(bulk_size=10)


async def scrape_steam_reviews(rate_limit: dict = None):
    """Scrape all reviews from steam for scraped games. This method is used to get initial data for system"""
    async with async_session() as session:
        async with SteamScraper(rate_limit=rate_limit) as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_all_reviews_for_not_updated_steam_games()


async def main():
    parser = argparse.ArgumentParser('dataset.py')
    parser.add_argument('--steam-games', action='store_true')
    parser.add_argument('--steam-reviews', action='store_true')
    parser.add_argument('--doupe-reviews', action='store_true')
    parser.add_argument('--gamespot-reviews', action='store_true')
    parser.add_argument('--rate-limit', default=None, type=int, help="Use rate limit for scraper in requests/sec")
    args = parser.parse_args()

    rate_limit = None
    if args.rate_limit:
        rate_limit = {"max_rate": args.rate_limit, "time_period": 1}

    if args.steam_games:
        if rate_limit is not None:
            await scrape_steam_games(rate_limit=rate_limit)
    elif args.steam_reviews:
        if rate_limit is not None:
            await scrape_steam_reviews(rate_limit=rate_limit)
    elif args.doupe_reviews:
        if rate_limit is not None:
            await scrape_doupe_reviews(rate_limit=rate_limit)
    elif args.gamespot_reviews:
        if rate_limit is not None:
            await scrape_gamespot_reviews(rate_limit=rate_limit)
    else:
        parser.print_help()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
