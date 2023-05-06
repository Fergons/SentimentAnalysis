import argparse
import asyncio
import logging
import random
from datetime import timedelta
from typing import List, Optional, Union, TypeVar, Tuple, Literal, Any, Dict

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import async_session

import app.models as models
from .scraper import SteamScraper, Scraper, DoupeScraper, GamespotScraper
from .constants import STEAM_REVIEWS_API_RATE_LIMIT, STEAM_API_RATE_LIMIT, DEFAULT_RATE_LIMIT
from app.core.config import settings
from sqlalchemy import exc, and_
from app import crud, schemas

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger("scraper_to_db.py")


class DBScraper:
    @classmethod
    async def create(cls, scraper: Scraper = None, session: AsyncSession = None):
        self = DBScraper()
        self.scraper = scraper
        self.session = session
        self.db_source = await crud.source.get_by_url(self.session, url=self.scraper.url)
        if self.db_source is None:
            raise ValueError(f"Source {self.scraper.url} was not found in db!")
        return self

    def __init__(self):
        self.scraper = None
        self.session: Optional[AsyncSession] = None
        self.db_source = None

    async def scrape_games(self, num_games: Optional[int] = 1000, **kwargs) -> List[str]:
        blacklist = await crud.game.get_all_app_ids_from_source(self.session, source_id=self.db_source.id)
        new_games_in_db = []
        async for page in self.scraper.games_page_generator(page_size=kwargs.get("page_size", 100),
                                                            blacklist=blacklist):
            scraped_games = [schemas.ScrapedGame(source_id=self.db_source.id, **game.dict(by_alias=True)) for game in
                             page if game is not None]
            db_games = await self.add_games_to_db(scraped_games)
            await self.session.commit()
            logger.info(f"Added {list(db_games.keys())} games to db!")
            new_games_in_db += db_games.keys()
            if num_games is not None and len(new_games_in_db) >= num_games:
                break

        return new_games_in_db

    async def add_games_to_db(self, scraped_games: List[schemas.ScrapedGame]) -> Dict[str, models.Game]:
        source_game_ids = [game.source_game_id for game in scraped_games]
        db_games = await crud.game.get_by_source_game_ids(self.session,
                                                          source_id=self.db_source.id,
                                                          source_game_ids=source_game_ids)
        logger.debug(f"Found {list(db_games.keys())} games in db!")
        for game in scraped_games:
            source_game_id = game.source_game_id
            if source_game_id in db_games:
                continue
            if game.type != "game":
                # add non-game app to db if not already there (only steam has non-game apps mixed with games)
                # first check if it's already in db because of another concurrent scraper
                db_gamesource = await crud.game.get_by_source_id(self.session, source_id=self.db_source.id,
                                                                 source_game_id=source_game_id)
                if db_gamesource is None:
                    await crud.source.add_game(self.session, source_id=self.db_source.id, source_game_id=source_game_id)
                continue
            game = await crud.scraper.store_game_with_additional_objects(self.session, scraped_obj=game)
            db_games[source_game_id] = game
        return db_games

    async def add_reviews_to_db(self, scraped_reviews: List[schemas.ScrapedReview]) -> Dict[str, models.Review]:
        review_ids = [str(r.source_review_id) for r in scraped_reviews]
        query_reviews = select(models.Review.id, models.Review.source_review_id) \
            .where(and_(models.Review.source_id == self.db_source.id,
                        models.Review.source_review_id.in_(review_ids)))
        db_review_ids = await self.session.execute(query_reviews)
        db_review_ids = {source_id: db_id for db_id, source_id in db_review_ids.all()}
        for review in scraped_reviews:
            source_review_id = review.source_review_id
            if source_review_id in db_review_ids.keys():
                continue
            review = await crud.scraper.store_review_with_additional_objects(self.session, scraped_obj=review)
            db_review_ids[source_review_id] = review.id
        return db_review_ids

    async def add_reviewers_to_db(self, scraped_reviewers: List[BaseModel]) -> Dict[str, models.Reviewer]:
        data = [reviewer.dict(by_alias=True) for reviewer in scraped_reviewers]
        source_reviewer_ids = [reviewer.get("source_reviewer_id") for reviewer in data]
        db_reviewer_ids = await crud.reviewer.get_ids_by_source_reviewer_ids(self.session,
                                                                             source_id=self.db_source.id,
                                                                             source_reviewer_ids=source_reviewer_ids)
        db_reviewers = {}
        for reviewer in data:
            source_reviewer_id = reviewer.get("source_reviewer_id")
            obj_data = schemas.Reviewer(**reviewer).dict()
            db_id = db_reviewer_ids.get(source_reviewer_id, None)
            db_reviewer = models.Reviewer(**obj_data)
            db_reviewer.id = db_id
            db_reviewers[source_reviewer_id] = db_reviewer

        self.session.add_all(db_reviewers.values())
        return db_reviewers

    async def scrape_reviews_for_game(
            self,
            game_id: int = None,
            source_game_id: str = None,
            day_range: int = None,
            language: str = "czech",
            max_reviews: Optional[int] = 100,
            **kwargs
    ) -> Tuple[int, int]:
        num_reviews_scraped = 0
        if source_game_id is None and game_id is None:
            raise ValueError("Either game_id or source_game_id must be provided!")
        if game_id is None:
            ids = await crud.game.get_ids_by_source_game_ids(self.session,
                                                             source_id=self.db_source.id,
                                                             source_game_ids=[source_game_id])
            game_id = ids.get(source_game_id)
            logger.debug(f"The game is not in the db yet: {ids}")
            logger.debug(f"Scraping game with source_game_id {source_game_id}...")
            scraped_game = await self.scraper.get_game_info(source_game_id)
            if not scraped_game:
                raise ValueError(f"Game with source_game_id {source_game_id} not found!")
            scraped_game = schemas.ScrapedGame(source_id=self.db_source.id, **scraped_game.dict(by_alias=True))
            db_game = await self.add_games_to_db([scraped_game])
            game_id = db_game[source_game_id].id
        if source_game_id is None:
            source_game_id = await crud.game.get_source_game_id(self.session, id=game_id)

        async for page in self.scraper.game_reviews_page_generator(
                game_id=source_game_id,
                language=language,
                day_range=day_range,
                max_reviews=max_reviews, **kwargs):
            num_reviews_scraped += len(page)
            reviews = [
                schemas.ScrapedReview(game_id=game_id, source_id=self.db_source.id, **review.dict(by_alias=True)) for
                review in page]
            db_review_ids = await self.add_reviews_to_db(reviews)

        await crud.game.update_after_reviews_scrape(self.session, source_id=self.db_source.id, game_id=game_id)
        return game_id, num_reviews_scraped

    async def scrape_all_reviews_for_not_updated_steam_games(self, game_ids: List[str] = None,
                                                             check_interval: timedelta = None,
                                                             max_reviews: int = 100000):
        if game_ids is None:
            games = await crud.game.get_ids_and_source_ids_for_reviews_scraping_from_source(
                self.session,
                source_id=self.db_source.id,
                check_interval=check_interval
            )
            random.shuffle(games)
            game_ids = {game[1]: game[0] for game in games}

        for source_game_id, game_id in game_ids.items():
            logger.info(f"Scraping for game {source_game_id} started.")
            _, num_reviews_scraped = await self.scrape_reviews_for_game(game_id=game_id,
                                                                        source_game_id=source_game_id,
                                                                        max_reviews=1000000)
            logger.info(f"Scraping for game {source_game_id} finished. Scraped {num_reviews_scraped} reviews!")

    async def scrape_all_reviews(self, max_reviews: int = 100):
        async for page in self.scraper.game_reviews_page_generator(max_reviews=max_reviews):
            objs_in = []

            for review in page:
                review_data = review.dict(by_alias=True)
                review_obj = schemas.Review.parse_obj(review_data)
                review_obj.source_id = self.db_source.id

                if review_data.get("game") is not None:
                    game_data = review.game.dict(by_alias=True)
                    source_game_id = game_data.get("source_game_id")
                    game_obj = schemas.Game.parse_obj(game_data)
                    db_game = await crud.game.get_by_source_id(self.session,
                                                               source_id=self.db_source.id,
                                                               source_game_id=source_game_id)

                    if db_game is None:
                        db_game = await crud.game.create_from_source(self.session,
                                                                     obj_in=game_obj,
                                                                     source_id=self.db_source.id,
                                                                     source_game_id=source_game_id)
                    review_obj.game_id = db_game.id

                if review_data.get("reviewer") is not None:
                    reviewer_data = review.reviewer.dict(by_alias=True)
                    review_obj.playtime_at_review = reviewer_data.get("playtime_at_review")

                    reviewer_obj = schemas.Reviewer.parse_obj(reviewer_data)
                    reviewer_obj.source_id = self.db_source.id

                    db_reviewer = await crud.reviewer.get_by_source_id(self.session,
                                                                       source_id=self.db_source.id,
                                                                       source_obj_id=reviewer_obj.source_reviewer_id)
                    if db_reviewer is None:
                        db_reviewer = await crud.reviewer.create_from_source(obj_in=reviewer_obj)
                    reviewer_obj.id = db_reviewer.id

                objs_in.append(review_obj)
                if len(objs_in) >= max_reviews:
                    break
            await crud.review.create_multi(self.session, objs_in=objs_in)


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


async def scrape_steam_games(rate_limit: dict = None, **kwargs):
    """Scrape all games from steam. This method is used to get initial data for system"""
    if rate_limit is None:
        rate_limit = STEAM_API_RATE_LIMIT
    async with async_session() as session:
        async with SteamScraper(rate_limit=rate_limit) as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_games(**kwargs)


async def scrape_steam_reviews(rate_limit: dict = None, check_interval: timedelta = timedelta(days=7)):
    """Scrape all reviews from steam for scraped games. This method is used to get initial data for system"""
    async with async_session() as session:
        async with SteamScraper(rate_limit=rate_limit) as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_all_reviews_for_not_updated_steam_games(check_interval=check_interval)


async def scrape_steam_reviews_for_game(rate_limit: dict = None, **kwargs):
    """Scrape all reviews from steam for specific game. This method is used to get initial data for system"""
    logger.debug(f"Creating db session: In progress.")
    async with async_session() as session:
        logger.debug(f"Creating db session: Done.")
        logger.debug(f"Creating scraper: In progress.")
        async with SteamScraper(rate_limit=rate_limit) as scraper:
            logger.debug(f"Creating scraper: Done.")
            logger.debug(f"Creating db scraper: In progress.")
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            logger.debug(f"Creating db scraper: Done.")
            await db_scraper.scrape_reviews_for_game(**kwargs)


async def main():
    parser = argparse.ArgumentParser('dataset.py')
    parser.add_argument('--steam-games', action='store_true')
    parser.add_argument('--steam-reviews', action='store_true')
    parser.add_argument('--doupe-reviews', action='store_true')
    parser.add_argument('--gamespot-reviews', action='store_true')
    parser.add_argument('--rate-limit', default=None, type=int, help="Use rate limit for scraper in requests/sec")
    parser.add_argument('--check-interval', default=7, type=int, help="Check interval for scraper in days")
    parser.add_argument('--max-reviews', default=None, type=int, help="Max reviews to scrape")
    parser.add_argument('--game-id', default=None, type=int, help="Game id to scrape reviews for")
    parser.add_argument('--source-game-id', default=None, type=str,
                        help="Game id based on source (eg. review url or id  on the actual site) to scrape reviews for")
    parser.add_argument('--max-games', default=None, type=int, help="Max games to scrape")
    parser.add_argument('--page-size', default=1, type=int, help="Page size for scraper")
    parser.add_argument('--language', default='english,czech', type=str, help="Language of the reviews")
    args = parser.parse_args()

    rate_limit = None
    if args.rate_limit:
        rate_limit = {"max_rate": args.rate_limit, "time_period": 1}
    try:

        if args.steam_games:
            logger.info("Started scraping steam games")
            await scrape_steam_games(rate_limit=rate_limit, num_games=args.max_games, page_size=args.page_size)
        elif args.steam_reviews:
            if args.game_id is not None or args.source_game_id is not None:
                logger.info(f"Started scraping steam reviews for game {args.game_id}")
                await scrape_steam_reviews_for_game(
                    game_id=args.game_id,
                    source_game_id=args.source_game_id,
                    rate_limit=rate_limit,
                    max_reviews=args.max_reviews,
                    language=args.language)
            else:
                logger.info("Started scraping steam reviews")
                await scrape_steam_reviews(rate_limit=rate_limit)
        elif args.doupe_reviews:
            logger.info("Started scraping doupe reviews")
            await scrape_doupe_reviews(rate_limit=rate_limit)
        elif args.gamespot_reviews:
            logger.info("Started scraping gamespot reviews")
            await scrape_gamespot_reviews(rate_limit=rate_limit)
        else:
            parser.print_help()
    except Exception as e:
        raise e
    finally:
        logger.info("Finished")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
