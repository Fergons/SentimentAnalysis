import logging

from typing import Union, List, Callable, Tuple, Iterable, Any, Optional

import httpx
from http import HTTPStatus
from .constants import ContentType, STEAM_API_RATE_LIMITS
from aiolimiter import AsyncLimiter
from datetime import date
from datetime import datetime
from app.schemas.game import GameUpdate
import asyncio

logger = logging.getLogger("scraper.py")


class Scraper:
    @staticmethod
    def json_response_validator(r):
        return r.status_code == HTTPStatus.OK and "application/json" in r.headers.get("content-type", "")

    def __init__(self,
                 url: str = None,
                 games_endpoint: str = None,
                 game_reviews_endpoint: str = None,
                 game_info_endpoint: str = None,
                 reviewers_endpoint: str = None,
                 content_type: Union[str, ContentType] = None,
                 endpoints: dict = None,
                 is_api: bool = False,
                 auth: bool = False,
                 api_key: str = None,
                 session: Union[httpx.AsyncClient, httpx.Client, None] = None):
        self._url = url
        self.is_api = is_api
        self.content_type = content_type
        self.games_endpoint = games_endpoint
        self.game_info_endpoint = game_info_endpoint
        self.game_reviews_endpoint = game_reviews_endpoint
        self.reviewers_endpoint = reviewers_endpoint
        self.endpoints = endpoints or {}
        self.auth = auth
        self.api_key = api_key
        self.session: Union[httpx.AsyncClient, httpx.Client, None] = session

    async def __aenter__(self):
        self.session = httpx.AsyncClient()
        return self

    async def __aexit__(self, *args):
        await self.session.aclose()

    def handle_response(self,
                        response: httpx.Response,
                        validator: Callable = lambda r: SteamScraper.json_response_validator(r),
                        formatter: Callable = lambda r: r.json(),
                        validator_params: dict = {},
                        formatter_params: dict = {},
                        ) -> Any:
        if validator(response, **validator_params):
            return formatter(response, **formatter_params)

    async def get_game_reviews(self, game_id):
        pass

    async def get_games(self):
        pass

    async def get_game_info(self, game_id):
        pass

    async def get_reviewer_info(self, reviewer_id):
        pass

    async def _get_game_reviews_api(self, game_id):
        # async with httpx.AsyncClient() as client:
        #     r = await client.get('https://www.example.com/')
        # if r.status_code == HTTPStatus.OK:
        #     return r
        pass

    def _scrape_games(self):
        pass


class SteamScraper(Scraper):
    _url = "https://api.steampowered.com/"
    _games_endpoint = "https://api.steampowered.com/ISteamApps/GetAppList/v2"
    _game_info_endpoint = "https://store.steampowered.com/api/appdetails"
    _game_reviews_endpoint = "https://store.steampowered.com/appreviews"
    _reviewers_endpoint = "https://store.steampowered.com/appreviews/"
    _rate_limit = STEAM_API_RATE_LIMITS

    def __init__(self):
        super().__init__(url=self._url,
                         games_endpoint=self._games_endpoint,
                         game_info_endpoint=self._game_info_endpoint,
                         game_reviews_endpoint=self._game_reviews_endpoint,
                         reviewers_endpoint=self._reviewers_endpoint,
                         content_type=ContentType.JSON,
                         is_api=True)
        self.rate_limit = AsyncLimiter(**STEAM_API_RATE_LIMITS)
        self.request_counter = 0

    async def get_games(self):
        response = await self.session.get(self.games_endpoint)
        result = self.handle_response(response,
                                      self.json_response_validator,
                                      lambda r: r.json().get("applist", {}).get("apps"))
        if result is not None:
            return [app for app in result if app.get("name") != ""]

    @staticmethod
    def game_info_formatter(r, **params):
        r_json = r.json()
        game_id = params["game_id"]
        result = r_json.get(game_id)
        if not result.get("success", False):
            return None
        data = result.get("data")
        if data.get("type") == "game":
            return GameUpdate(
                name=data.get("name"),
                image_url=data.get("header_image"),
                release_date=datetime.strptime(data.get("release_date").get("date"), "%d %b, %Y"),
                category_names=[c.get("description") for c in data.get("categories", [])],
                source_app_id=data.get(game_id),
                source_url="https://store.steampowered.com",
            )

    async def get_game_info(self, game_id: Union[int, str]) -> GameUpdate:
        params = {
            "appids": game_id,
            "language": "eng"
        }

        async with self.rate_limit:
            logger.log(logging.DEBUG, f"Api call: get_game_info")
            response = await self.session.get(self.game_info_endpoint, params=params)

        return self.handle_response(response,
                                    self.json_response_validator,
                                    self.game_info_formatter,
                                    formatter_params={"game_id": str(game_id)})

    async def get_games_info(self, game_ids: Iterable[Union[str, int]]):
        tasks = [self.get_game_info(game_id) for game_id in game_ids]
        counter = 1
        for future in asyncio.as_completed(tasks):
            result: GameUpdate = await future
            # process(result)
            logger.log(logging.INFO, f"{counter}. results are from: {result.source_app_id}:{result.name}!")
            counter += 1

    @staticmethod
    def game_reviews_formatter(r):
        result = r.json()
        if not result.get("success", 0) == 1:
            raise StopAsyncIteration(result.get("error"))
        if result["query_summary"].get("total_reviews"):
            logger.log(logging.DEBUG, f"query_summary: {result['query_summary']}")
        return result["reviews"], result["query_summary"]["num_reviews"], result["cursor"]

    async def game_reviews_page_generator(self,
                               game_id: Union[str, int],
                               filter: Optional[str] = "recent",
                               language: Optional[str] = "czech",
                               day_range: Optional[int] = None,
                               review_type: Optional[str] = "all",
                               purchase_type: Optional[str] = "all",
                               cursor: Optional[str] = "*",
                               limit: int = 10000):

        params = {
            "json": 1,
            "filter": filter,
            "language": language,
            "day_range": day_range,
            "cursor": cursor,
            "review_type": review_type,
            "purchase_type": purchase_type,
            "num_per_page": limit if limit <= 100 else 100
        }

        params = {k: v for k, v in params.items() if v is not None}
        while limit > 0:
            async with self.rate_limit:
                response = await self.session.get(f"{self.game_reviews_endpoint}/{game_id}", params=params)

            logger.log(logging.INFO, f"api call({self.request_counter}):{game_id}: {response.url}")
            result = self.handle_response(response, formatter=self.game_reviews_formatter)
            if result is None:
                logger.log(logging.INFO, f"no result StopAsyncIteration ")
                break

            reviews, num_reviews, cursor = result

            if params.get("cursor") is None or params.get("cursor") == cursor:
                logger.log(logging.INFO, f"cursor StopAsyncIteration {result}")
                break
            # new cursor received which implies theres is more content but no data in response ->
            # fallback to previous call
            if num_reviews == 0:
                continue

            params["cursor"] = cursor
            limit -= num_reviews
            logger.log(logging.DEBUG, f"api call({self.request_counter}):{game_id}: get_game_reviews yield")
            self.request_counter += 1
            yield reviews

    async def get_game_reviews(self, game_id, **kwargs):
        all_reviews = []
        # filter = lambda x: x if x.get("recommendationid") not in review_ids else None
        async for page in self.game_reviews_page_generator(game_id, **kwargs):
            # process
            # ...
            all_reviews.extend(page)
        return game_id, len(all_reviews)

    async def get_games_reviews(self,
                                game_ids: Iterable[Union[str, int]],
                                query_params: Iterable[dict]):
        tasks = [self.get_game_reviews(game_id, **params) for game_id, params in zip(game_ids, query_params)]
        counter = 1
        for future in asyncio.as_completed(tasks):
            result = await future
            game_id, num_reviews = result
            logger.log(logging.INFO, f"{counter}. results are from: {game_id} num_reviews: {num_reviews}!")
            counter += 1



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete()
    #
    # except KeyboardInterrupt:
    #     loop.stop()
    #     pass
