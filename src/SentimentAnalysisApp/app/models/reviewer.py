from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Reviewer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    source_reviewer_id = Column(String)
    source_id = Column(Integer, ForeignKey('source.id'))
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    num_games_owned = Column(Integer)
    num_reviews = Column(Integer)
    # one(user) to many(reviews)
    # games = relationship("GameReviewer", back_populates="reviewer", cascade="all, delete")
    reviews = relationship("Review", back_populates="reviewer")
    source = relationship("Source", back_populates="reviewers")

    UniqueConstraint(source_reviewer_id, source_id)


# class GameReviewer(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     game_id = Column(Integer, ForeignKey('game.id'))
#     reviewer_id = Column(Integer, ForeignKey('reviewer.id'))
#     reviewer = relationship("Reviewer", back_populates="games")
#     game = relationship("Game", back_populates="reviewers")