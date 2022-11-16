import os

import logging
from pydantic import ValidationError

from typing import Union, List, Callable, Tuple, Iterable, Any, Optional

import httpx
from http import HTTPStatus
from .constants import ContentType, STEAM_API_RATE_LIMIT, SOURCES, SourceName, DEFAULT_RATE_LIMIT, SteamAppDetail, \
    SteamAppDetailResponse, SteamAppReviewsResponse
from aiolimiter import AsyncLimiter
from datetime import date
from datetime import datetime

import asyncio

logger = logging.getLogger("scraper.py")


class Scraper:
    @staticmethod
    def json_response_validator(r: httpx.Response):
        return r.status_code == HTTPStatus.OK and ContentType.JSON in r.headers.get(ContentType.alias, "")

    @staticmethod
    def xml_response_validator(r: httpx.Response):
        return r.status_code == HTTPStatus.OK and ContentType.XML in r.headers.get(ContentType.alias, "")

    @staticmethod
    def html_response_validator(r: httpx.Response):
        return r.status_code == HTTPStatus.OK and ContentType.HTML in r.headers.get(ContentType.alias, "")

    def __init__(self,
                 url: str = None,
                 user_reviews_url: Optional[str] = None,
                 critic_reviews_url: Optional[str] = None,
                 game_detail_url: Optional[str] = None,
                 list_of_games_url: Optional[str] = None,
                 reviewer_detail_url: Optional[str] = None,
                 list_of_reviewers_url: Optional[str] = None,
                 content_type: Union[str, ContentType] = None,
                 endpoints: Optional[dict] = None,
                 is_api: bool = False,
                 auth: bool = False,
                 api_key: Optional[str] = None,
                 session: Union[httpx.AsyncClient, httpx.Client, None] = None,
                 rate_limit: dict = DEFAULT_RATE_LIMIT,
                 **kwargs):

        self.url = url
        self.is_api = is_api
        self.content_type = content_type

        self.user_reviews_url = user_reviews_url
        self.critic_reviews_url = critic_reviews_url

        self.list_of_reviewers_url = list_of_reviewers_url
        self.reviewer_detail_url = reviewer_detail_url

        self.game_detail_url = game_detail_url
        self.list_of_games_url = list_of_games_url

        self.endpoints = endpoints or {}

        self.auth = auth
        self.api_key = api_key
        self.session: Union[httpx.AsyncClient, httpx.Client, None] = session
        self.rate_limit = AsyncLimiter(**rate_limit)
        self.request_counter = 0

        self.default_request_params = {"api_key": self.api_key} if self.api_key is not None else {}

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
    _source = SOURCES[SourceName.STEAM]
    _rate_limit = STEAM_API_RATE_LIMIT

    def __init__(self):
        super().__init__(content_type=ContentType.JSON,
                         is_api=True,
                         rate_limit=self._rate_limit,
                         **self._source)

    async def get_games(self):
        response = await self.session.get(self.list_of_games_url)
        result = self.handle_response(response,
                                      self.json_response_validator,
                                      lambda r: r.json().get("applist", {}).get("apps"))
        if result is not None:
            return [app for app in result if app.get("name") != ""]

    @staticmethod
    def game_info_formatter(r, **params) -> Optional[SteamAppDetail]:
        r_json = r.json()
        try:
            return [SteamAppDetailResponse.parse_obj(detail).data for app, detail in r_json.items()][0]
        except ValidationError as e:
            logger.log(logging.DEBUG, e)
            return None

    async def get_game_info(self, game_id: Union[int, str]) -> SteamAppDetail:
        params = {
            "appids": game_id,
            "language": "eng"
        }

        async with self.rate_limit:
            logger.log(logging.DEBUG, f"Api call: get_game_info")
            response = await self.session.get(self.game_detail_url, params=params)

        return self.handle_response(response,
                                    self.json_response_validator,
                                    self.game_info_formatter)

    async def get_games_info(self, game_ids: Iterable[Union[str, int]]) -> List[SteamAppDetail]:
        tasks = [self.get_game_info(game_id) for game_id in game_ids]
        counter = 1
        results = []
        for future in asyncio.as_completed(tasks):
            result: Optional[SteamAppDetail] = await future
            # process(result)
            logger.log(logging.DEBUG, result)
            logger.log(logging.INFO, f"Progress {counter}/{len(tasks)} tasks done!")
            if result is not None:
                results.append(result)
            counter += 1
        return results


    @staticmethod
    def game_reviews_formatter(r):
        result = r.json()
        return SteamAppReviewsResponse.parse_obj(result)
        # if not result.get("success", 0) == 1:
        #     raise StopAsyncIteration(result.get("error"))
        # if result["query_summary"].get("total_reviews"):
        #     logger.log(logging.DEBUG, f"query_summary: {result['query_summary']}")
        # return result["reviews"], result["query_summary"]["num_reviews"], result["cursor"]

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
                response = await self.session.get(f"{self.user_reviews_url}/{game_id}", params=params)

            logger.log(logging.INFO, f"api call({self.request_counter}):{game_id}: {response.url}")
            result: SteamAppReviewsResponse = self.handle_response(response, formatter=self.game_reviews_formatter)
            if result is None:
                logger.log(logging.INFO, f"no result StopAsyncIteration ")
                break

            reviews, num_reviews, cursor = result.reviews, result.query_summary.num_reviews, result.cursor

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
            logger.log(logging.INFO, f"Progress {counter}/{len(tasks)} tasks done!")
            counter += 1


class GamespotScraper(Scraper):
    _source = SOURCES[SourceName.GAMESPOT]
    _rate_limit = DEFAULT_RATE_LIMIT
    _api_key = os.environ.get("GAMESPOT_API_KEY")

    def __init__(self):
        super().__init__(content_type=ContentType.XML,
                         is_api=True,
                         api_key=self._api_key,
                         rate_limit=self._rate_limit,
                         **self._source)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete()
    #
    # except KeyboardInterrupt:
    #     loop.stop()
    #     pass