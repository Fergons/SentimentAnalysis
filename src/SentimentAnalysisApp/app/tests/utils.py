import random
import string
from typing import List

from pydantic import AnyHttpUrl
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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


async def create_sources(session: AsyncSession) -> List[schemas.Source]:
    results = []
    for name, value in SOURCES.items():
        new_source = await crud.source.create(session, obj_in=schemas.SourceCreate(**value))
        results.append(new_source)
    assert len(results) == len(SOURCES.keys())

    result = await session.execute(select(models.Source))
    assert len(result.scalars().all()) == len(SOURCES.keys())
    return results


async def create_game():

    return await crud.game.create(
        schemas.GameCreate(
            name=random_lower_string(),
            image_url=random_http_url(),
            source_id=1,
            source_game_id=str(random.randint(123213, 24331413))
        )
    )

