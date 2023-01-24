import requests as re
import json
from enum import Enum
from lxml import etree
import asyncio
import logging
from functools import partial
from dateutil import parser as date_parser
from bs4 import BeautifulSoup
from pydantic import BaseModel

class ReviewSource(Enum):
    STEAM = 'steam'
    METACRITIC = 'metacritic'
    GAMESPOT = 'gamespot'
    ALL = 'all'


def review_filter(reviews):
    filtered_reviews = set(reviews)
    filtered_reviews = filter(lambda x: len(x) > 1, filtered_reviews)
    return list(filtered_reviews)


def save_json(filename, data, **kwargs):
    with open(filename, "w", encoding="utf-8") as fopen:
        json.dump(data, fopen, **kwargs)

def save_text(filename, data):
    with open(filename, "w", encoding="utf-8") as fopen:
        fopen.write(data)


def download_json(appid, language="czech", day_range=10000):
    params = {"language": language,
              "filter": "recent",
              "purchase_type": "all",
              "num_per_page": 100,
              "day_range": day_range}
    used_cursors = []

    reviews = []
    filename = f"../data/appid_{appid}_{language}.json"
    with open(filename, "w", encoding="utf-8") as fopen:
        while True:
            response = re.get(f"https://store.steampowered.com/appreviews/{appid}?json=1", params=params)
            response_json = response.json()
            query_summary = response_json.get("query_summary")
            success = response_json.get("success", 0)
            print(f"Reponse summary: {query_summary}")
            reviews += [review.get("review", "").encode("utf-8").decode("utf-8") for review in
                        response_json.get("reviews", {})]  # if review.get("voted_up")]
            params["cursor"] = response_json.get("cursor")
            if success == 1:
                if params["cursor"] in used_cursors:
                    break
                else:
                    used_cursors.append(params["cursor"])

            if len(reviews) >= 10000:
                break

            print(f"Got {len(reviews)} reviews.\r")

        json.dump(review_filter(reviews), fopen, ensure_ascii=False)


def process_json(appid, language):
    with open(f"../data/appid_{appid}_{language}.json", "r") as fopen:
        review_list = json.load(fopen)

    with open(f"../data/appid_{appid}_{language}.txt", "w", encoding="utf8") as fopen:
        for review in review_list:
            fopen.write(" ".join(review.split()))
            fopen.write("\n")


# get all app ids on steam at https://api.steampowered.com/ISteamApps/GetAppList/v2/
async def get_steam_app_ids(session=None, *args, **kwargs):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    async with session.get(url=url) as response:
        if response.status == 200:
            response_json = await response.json()
            save_json("../data/appid_list.json", response_json)
        else:
            pass


async def get_gamespot_review_by_steam_app_id(session=None, app_id=None, *args, **kwargs):
    if app_id is None:
        return None
    url = "http://www.gamespot.com/api/games/"
    params = {
        "api_key": GAMESPOT_API_KEY,
        "filter": f"name:"
    }

    async with session.get(url=url) as response:
        if response.status == 200:
            response_bytes = await response.read()
            xml_tree = process_gamespot_api_response(response_bytes)
            if xml_tree is not None:
                if xml_tree.find("deck").text == "":
                    return None
                else:
                    return
            else:
                return None
        else:
            pass


def process_gamespot_api_response(data):
    tree = etree.fromstring(data)
    response_code = int(tree.find("status_code").text)
    if response_code != 1:
        return None
    else:
        return tree


async def get_steam_reviews_for_app_id(session=None, app_id=None, *args, **kwargs):
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    params = {
        "json": 1
    }
    # add parameters to api request
    params.update(kwargs)

    async with session.get(url=url) as response:
        if response.status == 200:
            response_json = await response.json()


async def get_gamespot_reviews(session=None, *args, **kwargs):
    url = ""
    async with session.get() as response:
        pass


async def get_metacritic_reviews(session=None, *args, **kwargs):
    pass


# set because of psycopg3 that can not run in default asyncio Event Loop
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# self.loop = asyncio.get_event_loop()


class MainSystem:
    def __init__(self):
        pass


class GamesInfoGetter:
    """
    Gets information for games in source_game_id list.
    """

    def __init__(self, session=None):
        if session is None:
            raise TypeError("GamesInfoGetter: session is None. Please provide aiohttp.clientSession object.")
        self.session = session
        self.game_names = []
        self.gamespot_names = []
        self.metacritic_names = []
        self.steam_app_ids = None
        self.steam_blacklist_app_ids = None
        self.steam_app_dict = None
        self.config_filename = "../config/config.json"

    def get_config(self):
        try:
            with open(self.config_filename, "r") as fopen:
                return json.load(fopen)
        except FileNotFoundError:
            return None

    def load_config(self):
        config = self.get_config()
        if config is None:
            self.steam_blacklist_app_ids = set()
        else:
            self.steam_blacklist_app_ids = set(config.get("steam_blacklist_app_ids", []))

    def save_config(self):
        config = self.get_config()
        if config is None:
            config = {"steam_blacklist_app_ids": list(self.steam_blacklist_app_ids)}
        else:
            config["steam_blacklist_app_ids"] = list(self.steam_blacklist_app_ids)
        try:
            with open(self.config_filename, "w+") as fopen:
                json.dump(config, fopen)
        except Exception as e:
            logging.warning(f"Error: {e}")

    async def get_data(self, parser, url, sem=None, **kwargs):
        async with sem:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None
                else:
                    return await parser(response)

    async def parse_steam_app_info(self, response):
        response_json = await response.json()
        app_id, reply = response_json.popitem()
        if reply.get("success", False):
            return self.filter_steam_app_info(reply.get("data", {}))
        else:
            return None

    def filter_steam_app_info(self, data):
        if data.get("type", "not a game") != "game":
            return None
        release = data.get("release_date", {})
        if release.get("coming_soon", True) is True:
            return None
        else:
            release_date_string = release.get("date", "1 Jan, 2011")
            date = date_parser.parse(release_date_string, dayfirst=True)

            self.steam_blacklist_app_ids.update(data.get("dlc", []))
            self.steam_blacklist_app_ids.update([element["id"] for element in data.get("movies", [])])

            metacritic = data.get('metacritic')
            metacritic_user_reviews_url = None
            if metacritic is not None:
                metacritic_user_reviews_url = f"{metacritic.get('url').rsplit('?')[0]}/user-reviews"

            return {
                "name": data.get("name"),
                "steam_app_id": data.get("steam_appid"),
                "metacritic_user_reviews_url": metacritic_user_reviews_url,
                "image_url": data.get("header_image"),
                "release_timestamp": date
            }

    async def get_steam_games_info(self, *args, **kwargs):
        if "app_ids" in kwargs:
            app_ids = [id for id in kwargs["app_ids"] if id not in self.steam_blacklist_app_ids]
        elif args:
            app_ids = [id for id in args if id not in self.steam_blacklist_app_ids]
        else:
            raise TypeError("Expected app ids as positional arguments or list in keyword 'app_ids")
        if "sem" not in kwargs:
            sem = asyncio.Semaphore(5)
        else:
            sem = kwargs.get("sem")
        if len(app_ids) == 0:
            return None

        partial_func = partial(self.get_data, self.parse_steam_app_info, sem=sem)
        results = await asyncio.gather(*map(partial_func, map(self.create_steam_app_info_url, app_ids)))
        return results

    @staticmethod
    def create_steam_app_info_url(app_id):
        return f"https://store.steampowered.com/api/appdetails?appids={app_id}&language=english"

    async def search_steam_by_names(self, *args):
        if self.steam_app_dict is None:
            app_list = await get_steam_app_ids()
            self.steam_app_dict = dict(map(dict.popitem, app_list))
        for name in args:
            for app_id, value in self.steam_app_dict.items():
                if name == value:
                    yield app_id

    def search_gamespot_by_names(self, *args):
        pass

    def search_metacritic_by_names(self, *args):
        pass

    @staticmethod
    async def get_steam_app_ids(session):
        file_path = "../data/steam_appid_list.json"
        try:
            with open(file_path, "r") as fopen:
                steam_app_ids = json.load(fopen)
        except FileNotFoundError:
            async with session.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/") as response:
                if response.status == 200:
                    response_json = await response.json()
                    steam_app_ids = response_json.get("applist", {}).get("apps", {})
                    save_json(file_path, steam_app_ids)
                    return steam_app_ids
                else:
                    return None
        else:
            return steam_app_ids


class ReviewsGetter:
    def __init__(self, session=None, source=None, game_id=None):
        if source is None:
            raise TypeError("ReviewGetter source is None")
        if game_id is None:
            raise TypeError("ReviewGetter game_id is None")
        if session is None:
            raise TypeError("ReviewGetter session is None. Please provide aiohttp.clientSession object.")

        self.source = source
        self.session = session

        self.url = self.get_url()

    def __load_config__(self):
        pass

    async def get_reviews(self):
        if self.source == ReviewSource.STEAM:
            return await self.process_steam_reviews()
        elif self.source == ReviewSource.GAMESPOT:
            return await self.process_gamespot_reviews()
        elif self.source == ReviewSource.METACRITIC:
            return await self.process_metacritic_reviews()
        else:
            return None

    async def process_steam_reviews(self):
        params = {'json': 1}
        pass

    async def process_gamespot_reviews(self):
        pass

    async def process_metacritic_reviews(self):
        pass

    def get_url(self):
        return ""

    @classmethod
    def get_base_review_url_by_source(cls, source):
        if ReviewSource.STEAM:
            return "https://store.steampowered.com/appreviews/{}?json=1"
        elif ReviewSource.GAMESPOT:
            return "https://gamespot.com/appreviews/{}?json=1"
        elif ReviewSource.METACRITIC:
            return "https://metacritic.com/appreviews/{}?json=1"
        return


def get_meta():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = re.get("https://www.metacritic.com/game/pc/portal-2", headers=user_agent)
    print(r.content)


def main():
    download_json(appid="1938090", language="czech", day_range=20000)
    # async with aiohttp.ClientSession() as session:

    #     db = DatabaseHandler()
    #     getter = GamesInfoGetter(session=session)
    #     getter.load_config()
    #     apps_list = await getter.get_steam_app_ids(session)
    #     games_info = await getter.get_steam_games_info(530, 730, *map(lambda x: x["appid"], sample(apps_list, 1000)))
    #     if apps_list is not None:
    #         print(f"Number of apps retrieved: {len(apps_list)}.")
    #     else:
    #         print("No apps retrieved.")
    #     if games_info is None:
    #         print("No info retrieved")
    #     else:
    #         for info in games_info:
    #             if info is not None:
    #                 inserted = await db.update_game(**info)
    #                 if inserted:
    #                     getter.steam_blacklist_app_ids.update([info["steam_app_id"]])
    #         print(games_info)
    #     getter.save_config()


def get_languages_in_dict():
    language = {
        "english_name": "",
        "native_name": "",
        "api_code": "",
        "web_api_code": ""}
    languages = []
    r = re.get("https://partner.steamgames.com/doc/store/localization/languages")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.findAll('table')[0]
        print(table)
        for row in table.findAll("tr")[1:]:
            cols = row.findAll("td")
            languages.append(
                {"english_name": cols[0].text,
                 "native_name": cols[1].text,
                 "api_code": cols[2].text,
                 "web_api_code": cols[3].text})

    print(languages)
    save_json("../data/steam_languages.json", languages, ensure_ascii=False)

    if len(languages) > 0:
        with open("../data/python_enum_def_steam_languages.py", "w", encoding="utf-8") as fopen:
            lines1 = [f"class SteamApiLanguageCodes(str,Enum):\n"]
            lines2 = [f"class SteamWebApiLanguageCodes(str,Enum):\n"]
            for language in languages:
                lines1.append(f"    {language['api_code'].upper()} = \"{language['api_code']}\"\n")
                lines2.append(f"    {language['api_code'].upper()} = \"{language['web_api_code']}\"\n")
            fopen.writelines([*lines1, *lines2])
    return languages


def model_from_dict(model_name, d):
    object = [f"class {model_name}(BaseModel):\n"]
    objects = [object]
    for k,v in d.items():
        object.append(f"    {k}: {type(v).__name__}\n")
        if isinstance(v, dict):
            objects.extend(model_from_dict(k, v))
    return objects

# https://jsontopydantic.com/
def base_model_from_json_response():
    r = re.get("https://store.steampowered.com/api/appdetails?appids=730&json=1")
    data = r.json()
    objects = []

    if r.status_code == 200 and data.get("730",{}).get("success", False):
        objects.extend(model_from_dict("SteamAppDetailResponse",data))
        print(objects)
        with open("../data/response_appdetails_objects.txt", "w", encoding="utf-8") as fopen:
            for object in objects:
                fopen.writelines(object)
                fopen.write("\n\n")

    else:
        print("request failed")






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.get_event_loop().run_until_complete(main())

    # get_languages_in_dict()
    # base_model_from_json_response()
    main()