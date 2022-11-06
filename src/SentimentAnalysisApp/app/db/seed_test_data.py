"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if it does not exist.
"""

import asyncio
from typing import Optional

from fastapi_users.password import get_password_hash
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select

from datetime import datetime
from app import schemas
from app.core import config
from app.models.aspect import Aspect
from app.models.game import Game
from app.models.review import Review
from app.models.reviewer import Reviewer
from app.db.session import async_session

games = [
    {
    "id": 1,
    "steam_app_id": "730",
    "name": "CS:GO",
    "release_timestamp": datetime.now().astimezone()
    },
    {
    "id": 2,
    "steam_app_id": "530",
    "name": "Dota2",
    "release_timestamp": datetime.now().astimezone()
    }
]

reviewers = [
    {
        "id": 1,
        "num_steam_reviews": 30,
        "num_steam_games_owned": 30,
        "updated_at": datetime.now().astimezone()
    },
    {
        "id": 2,
        "num_steam_reviews": 21,
        "num_steam_games_owned": 3230,
        "updated_at": datetime.now().astimezone()
    },
    {
        "id": 3,
        "num_steam_reviews": 40,
        "num_steam_games_owned": 40,
        "updated_at": datetime.now().astimezone()
    }
]

reviews = [
    {
        "id": 1,
        "review_id": 40,
        "source_url": "example-source.com",
        "language": "czech",
        "review":   "Aight..   Well i think u need some luck or skill in this game...   Its rly cool if u meet some good  NOT toxic people in here...     But yeah like every single game it does have toxic community + smurfs hacker and whatever...   \n\n          ANYWAYS :: : : :   : : : : :: : :   IT  IS    A   REALLY    GOOD   GAME : : : :: : : : ::   APPROVED!  :DDDDDDD\n\n\n                   :DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD\n\n\nIts kinda fun..  playing with friends...",
        "summary": "Cool shit",
        "score": "7.5",
        "created_at":datetime.now().astimezone(),
        "processed_at":datetime.now().astimezone(),
        "apect_sum_polarity": "6.5"
    },
    {
        "id": 2,
        "review_id": 23,
        "source_url": "example-source.com",
        "language": "czech",
        "review":"Je to super hra, hlavně ve více lidech",
        "summary": "Cool shit",
        "score": "7.5",
        "created_at":datetime.now().astimezone(),
        "processed_at":datetime.now().astimezone(),
        "apect_sum_polarity": "6.2"
    }
]

aspects = [
    {
        "id": 1,
        "term": "příběhem",
        "category": "story",
        "polarity": "positive",
        "confidence": "0.85"
    },
    {
        "id": 2,
        "term": "hádanky",
        "category": "gameplay",
        "polarity": "positive",
        "confidence": "0.45"
    }
]


async def main() -> None:
    print("Seeding data")
    async with async_session() as session:
        game1 = Game(**games[0])
        game2 = Game(**games[1])

        user1 = Reviewer(**reviewers[0])
        user2 = Reviewer(**reviewers[1])
        user3 = Reviewer(**reviewers[2])

        review1 = Review(**reviews[0])
        review2 = Review(**reviews[1])

        aspect1 = Aspect(**aspects[0])
        aspect2 = Aspect(**aspects[1])

        review1.game = game1
        review2.game = game1

        review1.user = user1
        review2.user = user1

        review1.aspects.append(aspect1)
        review1.aspects.append(aspect2)

        try:
            session.add_all([game1,game2])
            session.add_all([user1, user2, user3])
            session.add_all([aspect1, aspect2])
            session.add_all([review1, review2])

            await session.commit()
        except Exception as e:
            print("Data already seeded.")
            raise
        else:
            print("Initial data seeded.")


if __name__ == "__main__":
    asyncio.run(main())