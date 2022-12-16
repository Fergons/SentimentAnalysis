import asyncio
import logging
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null

from app.crud.reviewer import crud_reviewer
from app.crud.base import CRUDBase
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewCreate, ReviewCreate
from app.schemas.reviewer import ReviewerCreate
from app.models.reviewer import Reviewer
from app.crud.game import crud_game
from app.models.game import Game
from app.models.source import GameSource



class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewCreate]):
    async def get_with_good_and_bad_by_language_multi(self, db: AsyncSession, *, language: str) -> List[Review]:
        result = await db.execute(select(Review).where((Review.language == "czech") &
                                                       ((Review.good is not None) | (Review.bad is not None)))
                                  )
        return result.scalars().all()

    async def get_by_user(self, db: AsyncSession, *, user_id: int) -> List[Review]:
        result = await db.execute(select(Review).where(Review.reviewer_id == user_id))
        return result.scalars().all()

    async def get_by_game(self, db: AsyncSession, *, game_id: int) -> List[Review]:
        result = await db.execute(select(Review).where(Review.game_id == game_id))
        return result.scalars().all()

    async def get_not_processed(self, db: AsyncSession, *, limit: int = 100, offset: int = 0) -> List[Review]:
        result = await db.execute(select(Review).where(Review.processed_at is None).limit(limit).offset(offset))
        return result.scalars().all()

    async def get_not_processed_by_source(self, db: AsyncSession,
                                          source_id: int,
                                          limit: int = 100,
                                          offset: int = 0) -> Optional[Review]:

        if offset > 2000:
            stmt = select(Review.id)\
                .where((Review.processed_at is None) & (Review.source_id == source_id))\
                .limit(limit).offset(offset)
            result_ids = await db.execute(stmt)
            ids = result_ids.scalars().all()
            stmt = select(Review).where(Review.id.in_(ids))
        else:
            stmt = select(Review).where((Review.processed_at == null()) & (Review.source_id == source_id))\
                .limit(limit).offset(offset)

        result = await db.execute(stmt)
        return result.scalars().all()

    async def create_with_text(
            self, db: AsyncSession, *, obj_in: ReviewCreate, text: str
    ) -> Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, text=text)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_reviewer(
        self, db: AsyncSession, *, obj_in: ReviewCreate, text:str,
    ) -> Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, text=text)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, *, objs_in: List[ReviewCreate], limit: int = 100):
        for obj in objs_in:
            db_obj = await self.get_by_source_id(db, obj.source_id, obj.source_review_id)
            if db_obj is not None:
                # possible update of the review in the DB
                continue

            db_obj = self.model(**obj.dict(exclude={"game", "reviewer"}))  # type: ignore
            if obj.game is not None:
                db_obj_game = await crud_game.create_from_source(db, obj_in=obj.game)
                db_obj.game_id = db_obj_game.id
            if obj.reviewer is not None:
                db_obj_reviewer = await crud_reviewer.create_from_source(db, obj_in=obj.reviewer)
                db_obj.reviewer_id = db_obj_reviewer.id

            db.add(db_obj)

        await db.commit()

    async def create_with_reviewer_multi(
            self, db: AsyncSession, *,
            objs_in: List[ReviewCreate],
            game_id: Optional[int] = None,
            source_id: Optional[int] = None,
            limit: int = 100):

        for obj in objs_in:
            db_obj = await self.get_by_source_id(db, obj.source_id, obj.source_review_id)
            if db_obj is not None:
                # possible update of the review in the DB
                continue
            reviewer_db_obj = await crud_reviewer.get_by_source_id(db, obj.source_id, obj.reviewer.source_reviewer_id)
            if reviewer_db_obj is None:
                obj.reviewer.source_id = obj.source_id
                reviewer_db_obj = Reviewer(**obj.reviewer.dict(exclude={"playtime_at_review"}))  # type: ignore
                db.add(reviewer_db_obj)
            obj.playtime_at_review = obj.reviewer.playtime_at_review
            db_obj = self.model(**obj.dict(exclude={"reviewer", "game"}))  # type: ignore
            db_obj.reviewer = reviewer_db_obj
            db.add(db_obj)

        await db.commit()

    async def create_with_game_multi(
            self, db: AsyncSession, *,
            objs_in: List[ReviewCreate]
    ):

        for obj in objs_in:
            db_obj = await self.get_by_source_id(db, obj.source_id, obj.source_review_id)
            if db_obj is not None:
                # possible update of the review in the DB
                continue
            game_db_obj = await crud_game.get_by_source_id(db, obj.source_id, obj.game.source_game_id)
            if game_db_obj is None:
                game_db_obj = await crud_game.get_by_name(db, name=obj.game.name)
                if game_db_obj is None:
                    game_db_obj = Game(**obj.game.dict(exclude={"source_id", "source_game_id"}))  # type: ignore

                game_source_db_obj = GameSource(
                    source_id=obj.source_id,            # type: ignore
                    source_game_id=str(obj.game.source_game_id)   # type: ignore
                )

                game_source_db_obj.game = game_db_obj
                db.add_all([game_db_obj, game_source_db_obj])

            db_obj = self.model(**obj.dict(exclude={"game", "reviewer"}))  # type: ignore
            db_obj.game = game_db_obj
            db.add(db_obj)

        await db.commit()


crud_review = CRUDReview(Review)
