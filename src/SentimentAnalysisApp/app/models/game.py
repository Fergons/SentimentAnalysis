from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class Game(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)

    release_date = Column(DateTime(timezone=True), default=None)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    # one(game) to many(reviews)
    reviews = relationship("Review", back_populates="game", lazy="selectin")
    sources = relationship("GameSource", back_populates="game", lazy="selectin")
    categories = relationship("GameCategory", back_populates="game", lazy="selectin")


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    games = relationship("GameCategory", back_populates="category", lazy="selectin")


class GameCategory(Base):
    id = Column(Integer, primary_key=True, index=True)

    game_id = Column(Integer, ForeignKey('game.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    game = relationship("Game", back_populates="categories", lazy="selectin")
    category = relationship("Category", back_populates="games", lazy="selectin")
