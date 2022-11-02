from backend.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    num_games_owned = Column(Integer)
    # one(user) to many(reviews)
    reviews = relationship("Review", back_populates="review")
