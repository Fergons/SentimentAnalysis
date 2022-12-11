from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, Computed, Index
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.ts_vector import TSVectorType



class Game(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    name_tsv = Column(
        TSVectorType("name", regconfig="english"),
        Computed("to_tsvector('english', \"name\")", persisted=True))
    image_url = Column(String)

    release_date = Column(DateTime(timezone=True), default=None)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    # one(game) to many(reviews)
    reviews = relationship("Review", back_populates="game", lazy="selectin")
    # reviewers = relationship("GameReviewer", back_populates="game", lazy="selectin", cascade="all, delete")
    sources = relationship("GameSource", back_populates="game", lazy="selectin", cascade="all, delete")
    categories = relationship("GameCategory", back_populates="game", lazy="selectin", cascade="all, delete")

    __table_args__ = (
        Index("idx_game_name_tsv", name_tsv, postgresql_using="gin"),
    )

class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    games = relationship("GameCategory", back_populates="category", lazy="selectin", cascade="all, delete")


class GameCategory(Base):
    id = Column(Integer, primary_key=True, index=True)

    game_id = Column(Integer, ForeignKey('game.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    game = relationship("Game", back_populates="categories", lazy="selectin")
    category = relationship("Category", back_populates="games", lazy="selectin")
