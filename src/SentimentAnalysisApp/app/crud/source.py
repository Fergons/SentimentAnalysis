from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceCreate


class CRUDSource(CRUDBase[Source, SourceCreate, SourceCreate]):
    def create_with_url(
            self, db: Session, *, obj_in: SourceCreate, url: str,
    ) -> Source:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, url=url)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


Source = CRUDSource(Source)
