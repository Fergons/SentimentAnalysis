import asyncio
from typing import Optional

from fastapi_users.password import get_password_hash
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select

from app.core import config
from app import crud, models, schemas
from app.models.user import User
from app.db.session import async_session
from app.services.scraper.constants import SOURCES

"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if it does not exist.
"""

async def main() -> None:
    print("Start initial data")
    async with async_session() as session:
        result = await session.execute(
            select(User).where(
                User.email == config.settings.FIRST_SUPERUSER_EMAIL
            )
        )
        user: Optional[User] = result.scalars().first()

        for name, value in SOURCES.items():
            source = await crud.source.get_by_name(session, name=name)
            if source is None:
                await crud.source.create(session, obj_in=schemas.SourceCreate(**value))
                print(f"Created source {name}.")
            else:
                print(f"Source {name} already exists")

        if user is None:
            await SQLAlchemyUserDatabase(schemas.UserDB, session, User).create(
                schemas.UserDB(
                    email=config.settings.FIRST_SUPERUSER_EMAIL,
                    is_superuser=True,
                    is_verified=True,
                    hashed_password=get_password_hash(
                        config.settings.FIRST_SUPERUSER_PASSWORD
                    ),
                )
            )
            print("Superuser was created")
        else:
            print("Superuser already exists in database")

        print("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
