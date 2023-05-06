import logging
from datetime import timedelta, datetime
from typing import List, Optional, Any, Tuple, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import column, update, func, cast, and_, text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count


from app import models, schemas
from .game import crud_game
from .game import crud_category
from .developer import crud_developer
from .review import crud_review
from .reviewer import crud_reviewer
from .source import crud_source

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
)
logger = logging.getLogger("scraper_db_IO")
class CRUDScraper:
    async def store_game(self, db: AsyncSession, *, scraped_obj: schemas.ScrapedGame) -> models.Game:
        """
        Stores a game
        """
        # validate scraped_game and transform to schemas
        game = await crud_game.get_by_source_id(db, source_id=scraped_obj.source_id,
                                                source_game_id=scraped_obj.source_game_id)
        if game:
            return game

        game_in = schemas.GameCreate(**scraped_obj.dict())
        game = await crud_game.create(db, obj_in=game_in)
        await crud_source.add_game(db, game_id=game.id, source_id=scraped_obj.source_id,
                                   source_game_id=scraped_obj.source_game_id)
        return game

    async def store_game_with_additional_objects(self, db: AsyncSession, *, scraped_obj: schemas.ScrapedGame) -> models.Game:
        """
        Stores a game with additional objects (categories, developers, etc.)
        and creates relationship objects between them.
        """
        # validate scraped_game and transform to schemas

        game_source = await crud_game.get_by_source_id(db, source_id=scraped_obj.source_id,
                                                source_game_id=scraped_obj.source_game_id)
        if game_source and game_source.game:
            return game_source.game

        game_in = schemas.GameCreate(**scraped_obj.dict())
        game = await crud_game.create(db, obj_in=game_in)

        if game_source:
            game_source.game_id = game.id
            await db.commit()
        else:
            await crud_source.add_game(db, game_id=game.id, source_id=scraped_obj.source_id,
                                       source_game_id=scraped_obj.source_game_id)

        if scraped_obj.categories:
            categories = await crud_category.create_multi_by_names(db,
                                                                   names=scraped_obj.categories)
            await crud_game.add_categories(db, game_id=game.id, categories=[c.id for c in categories])

        if scraped_obj.developers:
            developers = await crud_developer.create_multi_by_names(db,
                                                                    names=scraped_obj.developers)
            await crud_game.add_developers(db, game_id=game.id, developers=[d.id for d in developers])
        return game

    async def store_review(self, db: AsyncSession, *, scraped_obj: schemas.ScrapedReview) -> models.Review:
        """
        Stores a review
        """
        # validate scraped_review and transform to schemas
        review_in = schemas.ReviewCreate(**scraped_obj.dict(exclude_unset=True))
        review = await crud_review.create(db, obj_in=review_in)
        return review

    async def store_review_with_additional_objects(self, db: AsyncSession, *,
                                                   scraped_obj: schemas.ScrapedReview) -> models.Review:
        """
        Stores a review with additional objects (reviewer, game, etc.)
        """
        # check if review already exists
        review = await crud_review.get_by_source_id(db, source_id=scraped_obj.source_id, source_obj_id=scraped_obj.source_review_id)
        if review:
            return review

        # validate scraped_review and transform to schemas
        review_in = schemas.ReviewCreate(**scraped_obj.dict())
        review = await crud_review.create(db, obj_in=review_in, commit=False)
        if scraped_obj.reviewer:
            # check if in db
            reviewer = await crud_reviewer.get_by_source_id(db, source_id=scraped_obj.source_id, source_obj_id=scraped_obj.reviewer.source_reviewer_id)
            if not reviewer:
                reviewer_in = schemas.ReviewerCreate(**scraped_obj.reviewer.dict())
                reviewer = await crud_reviewer.create_from_source(db, obj_in=reviewer_in,
                                                                  source_id=scraped_obj.source_id,
                                                                  commit=False)
            review.reviewer = reviewer
            review.source_reviewer_id = scraped_obj.reviewer.source_reviewer_id
        if scraped_obj.game:
            game = await self.store_game_with_additional_objects(db, scraped_obj=scraped_obj.game)
            review.game_id = game.id

        await db.commit()
        return review


crud_scraper = CRUDScraper()
