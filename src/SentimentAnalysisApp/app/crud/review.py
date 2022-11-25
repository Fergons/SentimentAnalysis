from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewCreate


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewCreate]):
    def create_with_text(
            self, db: Session, *, obj_in: ReviewCreate, text:str,
    ) -> Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, text=text)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_review = CRUDReview(Review)
