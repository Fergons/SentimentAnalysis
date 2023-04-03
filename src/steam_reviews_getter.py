import os
import sys
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
import emoji
import re


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
    # ask user if he wants to re-download the reviews
    if os.path.exists(filename):
        print(f"File {filename} already exists. Do you want to re-download the reviews? [Y/n]")
        answer = input()
        if answer.lower() == "n":
            return

    with open(filename, "w", encoding="utf-8") as fopen:
        while True:
            response = re.get(f"https://store.steampowered.com/appreviews/{appid}?json=1", params=params)
            response_json = response.json()
            query_summary = response_json.get("query_summary")
            success = response_json.get("success", 0)
            print(f"Reponse summary: {query_summary}")
            reviews += response_json.get("reviews", {})
            params["cursor"] = response_json.get("cursor")
            if success == 1:
                if params["cursor"] in used_cursors:
                    break
                else:
                    used_cursors.append(params["cursor"])

            if len(reviews) >= 10000:
                break

            print(f"Got {len(reviews)} reviews.\r")

        json.dump(reviews, fopen, ensure_ascii=False)


def clean_text(text):
    """
    Removes unnecessary whitespaces, characters, emoticons, non ASCII characters, punctuation, normalizes to lowercase.
    :param text: string to clean
    :return: cleaned string
    """
    text = ' '.join(text.split())
    # remove graphical emoji
    text = emoji.replace_emoji(text)
    # remove textual emoji
    emoticon_string = r"(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP\/\:\}\{@\|\\]|[\)\]\(\[dDpP\/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"
    text = re.sub(emoticon_string, '', text)
    # remove links
    text = re.sub(r'https?\S+', '', text)
    # remove formatting
    # input: [h1] lorem ipsum [\h1]
    # output: lorem ipsum
    text = re.sub(r'\[[^]]*?]', '', text)

    # remove # and @
    for punc in '"#%&\'*<=>@[\\]^_`{|}~':
        text = text.replace(punc, '')

    # duplicit punctioation
    text = re.sub(r'([!?.,:;-]){2,}', r'\1', text)
    return text


def process_json(appid, language):
    with open(f"../data/appid_{appid}_{language}.json", "r", encoding="utf8") as fopen:
        review_list = json.load(fopen)

    with open(f"../data/appid_{appid}_{language}.txt", "w", encoding="utf8") as fopen:
        if type(review_list[0]) == dict:
            review_list = [review["review"] for review in review_list if review["voted_up"] is False]
        for review in review_list:
            if len(review) < 10 or len(review) > 200:
                continue
            fopen.write(" ".join(clean_text(review).strip().split()))
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


def get_meta():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = re.get("https://www.metacritic.com/game/pc/portal-2", headers=user_agent)
    print(r.content)


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
    for k, v in d.items():
        object.append(f"    {k}: {type(v).__name__}\n")
        if isinstance(v, dict):
            objects.extend(model_from_dict(k, v))
    return objects


# https://jsontopydantic.com/
def base_model_from_json_response():
    r = re.get("https://store.steampowered.com/api/appdetails?appids=730&json=1")
    data = r.json()
    objects = []

    if r.status_code == 200 and data.get("730", {}).get("success", False):
        objects.extend(model_from_dict("SteamAppDetailResponse", data))
        print(objects)
        with open("../data/response_appdetails_objects.txt", "w", encoding="utf-8") as fopen:
            for object in objects:
                fopen.writelines(object)
                fopen.write("\n\n")

    else:
        print("request failed")


def get_reviews_for_appid(appid="730"):
    download_json(appid=appid, language="czech", day_range=20000)
    process_json(appid=appid, language="czech")
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


if __name__ == "__main__":
    game_id = sys.argv[1]
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.get_event_loop().run_until_complete(main())

    # get_languages_in_dict()
    # base_model_from_json_response()
    get_reviews_for_appid(game_id)
