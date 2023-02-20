import datetime
import random
import string
from typing import List

from pydantic import AnyHttpUrl
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .test_data import (TEST_CATEGORY,
                        TEST_GAME,
                        TEST_GAME_CATEGORY,
                        TEST_GAME_SOURCE,
                        TEST_REVIEW,
                        TEST_REVIEWER,
                        TEST_SOURCE,
                        TEST_ASPECTS)

from app import schemas, crud, models
from app.models.user import User
from app.services.scraper.constants import SOURCES


def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(length: int = 10) -> str:
    return f"{random_lower_string(length)}@{random_lower_string(length)}.com"


def random_http_url() -> AnyHttpUrl:
    return AnyHttpUrl(scheme="https",
                      host=random_lower_string(),
                      path=random_lower_string(),
                      url=random_lower_string())

async def create_db_user(
    email: str,
    hashed_password: str,
    session: AsyncSession,
    is_superuser: bool = False,
    is_verified: bool = True,
) -> schemas.UserDB:

    new_user = await SQLAlchemyUserDatabase(schemas.UserDB, session, User).create(
        schemas.UserDB(
            email=EmailStr(email),
            is_superuser=is_superuser,
            is_verified=is_verified,
            hashed_password=hashed_password,
        )
    )
    return new_user


async def create_obj(session: AsyncSession, model, **kwargs) -> models.Source:
    for k, v in kwargs.items():
        if ("_at" in k or "_date" in k) and isinstance(v, str):
            # date format string for 2020-10-20 20:24:54.000000 +00:00
            kwargs[k] = datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f %z")
    db_obj = model(**kwargs) # type: ignore
    session.add(db_obj)
    await session.commit()
    return db_obj


async def create_objs(session: AsyncSession, model, objs: List[dict]) -> List[models.Source]:
    results = []
    for obj in objs:
        db_obj = await create_obj(session, model, **obj)
        results.append(db_obj)
    return results


async def seed_initial_test_data(session: AsyncSession):
    # seed table category
    categories = await create_objs(session, models.Category, TEST_CATEGORY)
    # seed table source
    sources = await create_objs(session, models.Source, TEST_SOURCE)
    # seed table game
    games = await create_objs(session, models.Game, TEST_GAME)
    # seed table game_source
    game_sources = await create_objs(session, models.GameSource, TEST_GAME_SOURCE)
    # seed table game_category
    game_categories = await create_objs(session, models.GameCategory, TEST_GAME_CATEGORY)
    # seed table reviewer
    reviewers = await create_objs(session, models.Reviewer, TEST_REVIEWER)
    # seed table review
    reviews = await create_objs(session, models.Review, TEST_REVIEW)
    # seed table aspect
    aspects = await create_objs(session, models.Aspect, TEST_ASPECTS)

    return {"category": categories,
            "source": sources,
            "game": games,
            "gamesource": game_sources,
            "gamecategory": game_categories,
            "reviewer": reviewers,
            "review": reviews,
            "aspect": aspects
            }

async def is_test_data_seeded(session: AsyncSession):
    result = await session.execute(select(models.Source))
    return len(result.scalars().all()) > 0