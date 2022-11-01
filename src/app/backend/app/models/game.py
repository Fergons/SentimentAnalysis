from backend.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


class Game(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    steam_app_id = Column(String, index=True)
    image_url = Column(String)
    release_timestamp = Column(DateTime(timezone=True), default=None)
    # sources
    metacritic_user_reviews_url = Column(String)
    gamespot_review_url = Column(String)
    gamespot_user_reviews_url = Column(String)
    # when was the last update for each source
    metacritic_updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    gamespot_updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    steam_updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    info_updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    # one(game) to many(reviews)
    reviews = relationship("Review", back_populates="review")
