from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class Source(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    url = Column(String, index=True)

    user_reviews_url = Column(String)
    critic_reviews_url = Column(String)

    game_detail_url = Column(String)
    list_of_games_url = Column(String)

    reviewer_detail_url = Column(String)
    list_of_reviewers_url = Column(String)

    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    reviews = relationship("Review", back_populates="source", lazy="selectin")
    reviewers = relationship("Reviewer", back_populates="source", lazy="selectin")
    games = relationship("GameSource", back_populates="source", lazy="selectin")


# mapping table between many to many relationship (Game <-> Source)
class GameSource(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    game_id = Column(Integer, ForeignKey('game.id'))
    source_id = Column(Integer, ForeignKey('source.id'))
    
    # source_game_id is the identification of the game in the source's DB
    source_game_id = Column(String, index=True, unique=True)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    game = relationship("Game", back_populates="sources", lazy="selectin")
    source = relationship("Source", back_populates="games", lazy="selectin")
