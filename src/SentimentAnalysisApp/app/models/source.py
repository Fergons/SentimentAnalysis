from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class Source(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    url = Column(String, index=True, unique=True)
    user_reviews_url = Column(String, unique=True)
    critic_reviews_url = Column(String, unique=True)
    
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    reviews = relationship("Review", back_populates="source")
    reviewers = relationship("Reviewers", back_populates="source")
    games = relationship("GameSource", back_populates="source")


# mapping table between many to many relationship (Game <-> Source)
class GameSource(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    game_id = Column(Integer, ForeignKey('game.id'))
    source_id = Column(String, ForeignKey('source.id'))
    
    # app_id is the identification of the game in the source's DB
    app_id = Column(String, index=True, unique=True) 
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    game = relationship("Game", back_populates="sources")
    source = relationship("Source", back_populates="games")