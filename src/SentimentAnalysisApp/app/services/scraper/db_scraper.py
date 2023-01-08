import argparse
import asyncio
import logging
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.crud.source import crud_source
from app.crud.review import crud_review
from app.schemas.game import GameCreate
from app.crud.game import crud_game
from app.schemas.review import ReviewCreate, ReviewCreate
from .scraper import SteamScraper, Scraper, DoupeScraper, GamespotScraper
from .gamespot_resources import GamespotRequestParams
from .steam_resources import SteamAppListResponse, SteamApp, SteamReview, SteamAppDetail
from .constants import STEAM_REVIEWS_API_RATE_LIMIT
from app.core.config import settings
from sqlalchemy import exc

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger("scraper_to_db.py")


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

    async def scrape_games(self, bulk_size: int = 20):
        db_game_ids = await crud_game.get_all_app_ids_from_source(self.session, source_id=self.db_source.id)
        logger.log(logging.DEBUG, f"{db_game_ids}")

        games: List[SteamApp] = await self.scraper.get_games()

        logger.log(logging.INFO, f"{len(db_game_ids)}/{len(games)} already in db!")
        group_counter = 1
        for bulk_start in range(0, len(games), bulk_size):
            tasks = []
            for game in games[bulk_start:bulk_start+bulk_size]:
                if str(game.appid) in db_game_ids:
                    continue
                tasks.append(self.scraper.get_game_info(game.appid))

            counter = 0
            for future in asyncio.as_completed(tasks):
                counter += 1
                detail: Optional[SteamAppDetail] = await future
                logger.log(logging.DEBUG, f"{type(detail)}: {detail}")
                if detail is None:
                    continue
                if detail.type != "game":
                    db_game = await crud_game.get_by_source_id(
                        self.session, source_id=self.db_source.id, source_game_id=detail.steam_appid)
                    if db_game is not None:
                        continue
                    try:
                        await crud_game.create_non_game_app_from_source(
                            self.session, source_id=self.db_source.id, source_obj_id=detail.steam_appid
                        )
                    except exc.IntegrityError as e:
                        logger.log(logging.ERROR, f"Integrity Error: {e}")
                    finally:
                        continue

                obj_in = GameCreate(
                    source_id=self.db_source.id,
                    **detail.dict(by_alias=True)
                )
                categories = [category.description for category in detail.categories]
                categories.extend([genre.description for genre in detail.genres])
                await crud_game.create_with_categories_by_names_and_source(
                    self.session, obj_in=obj_in, names=categories
                )
                logger.log(logging.INFO, f"Progress {counter}/{len(tasks)} tasks done!")

            logger.log(logging.INFO, f"Group {group_counter}/{len(games)//bulk_size} done!")
            group_counter += 1

    async def scrape_all_reviews_for_not_updated_games(self, game_ids: List[str] = None, max_reviews: int = 100000):
        games = await crud_game.get_all_not_updated_db_games_from_source(self.session, source_id=self.db_source.id)
        if game_ids is None:
            game_ids = {game.source_game_id: game.game.id for game in games}

        tasks = [self.scraper.get_game_reviews(game_id, **{"language": "czech", "limit": max_reviews}) for game_id in game_ids.keys()]
        counter = 1
        for future in asyncio.as_completed(tasks):
            result = await future
            game_id, reviews = result

            if len(reviews) > 0:
                review_create_objs = [
                    ReviewCreate(source_id=self.db_source.id, game_id=game_ids[game_id], **review.dict(by_alias=True))
                    for review in reviews
                ]
                await crud_review.create_multi(self.session, objs_in=review_create_objs)
                await crud_game.touch(self.session, obj_id=game_ids[game_id])

            logger.log(logging.INFO, f"{counter}. results are from: {game_id} num_reviews: {len(reviews)}!")
            logger.log(logging.INFO, f"Progress {counter}/{len(tasks)} tasks done!")
            counter += 1

    async def scrape_all_reviews(self, max_reviews: int = 100):
        async for page in self.scraper.game_reviews_page_generator(max_reviews=max_reviews):
            objs_in = []

            for review in page:
                review_obj = ReviewCreate.parse_obj(review.dict(by_alias=True))
                review_obj.source_id = self.db_source.id
                if review_obj.game is not None:
                    review_obj.game.source_id = self.db_source.id
                if review_obj.reviewer is not None:
                    review_obj.reviewer.source_id = self.db_source.id
                objs_in.append(review_obj)
                if len(objs_in) >= max_reviews:
                    break
            await crud_review.create_multi(self.session, objs_in=objs_in)


async def scrape_gamespot_reviews():
    """Scrape gamespot reviews. This method is used to get initial data for system"""
    async with async_session() as session:
        async with GamespotScraper(api_key=settings.GAMESPOT_API_KEY) as scraper:
            db_scraper = await DBScraper.create(scraper, session)
            await db_scraper.scrape_all_reviews()


async def scrape_doupe_reviews():
    """Scrape all reviews from doupe.cz. This method is used to get initial data for system"""
    async with async_session() as session:
        async with DoupeScraper() as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_all_reviews(max_reviews=2000)


async def scrape_steam_games():
    """Scrape all games from steam. This method is used to get initial data for system"""
    async with async_session() as session:
        async with SteamScraper(rate_limit={"max_rate": 2, "time_period": 3}) as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_games(bulk_size=100)


async def scrape_steam_reviews():
    """Scrape all reviews from steam for scraped games. This method is used to get initial data for system"""
    async with async_session() as session:
        async with SteamScraper() as scraper:
            db_scraper = await DBScraper.create(scraper=scraper, session=session)
            await db_scraper.scrape_all_reviews_for_not_updated_games()


async def main():

    parser = argparse.ArgumentParser('dataset.py')
    parser.add_argument('--steam-games', action='store_true')
    parser.add_argument('--steam-reviews', action='store_true')
    parser.add_argument('--doupe-reviews', action='store_true')
    parser.add_argument('--gamespot-reviews', action='store_true')

    args = parser.parse_args()

    if args.steam_games:
        await scrape_steam_games()
    elif args.steam_reviews:
        await scrape_steam_reviews()
    elif args.doupe_reviews:
        await scrape_doupe_reviews()
    elif args.gamespot_reviews:
        await scrape_gamespot_reviews()
    else:
        parser.print_help()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()