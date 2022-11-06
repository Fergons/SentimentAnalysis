from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


class Reviewer(Base):
    id = Column(Integer, primary_key=True, index=True)

    platform_id = Column(String)
    num_steam_reviews = Column(Integer)
    num_steam_games_owned = Column(Integer)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    # one(user) to many(reviews)
    reviews = relationship("Review", back_populates="user")
