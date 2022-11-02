from backend.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, TEXT
from sqlalchemy.orm import relationship


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    source_url = Column(String)

    language = Column(String)
    review = Column(TEXT)
    summary = Column(TEXT)
    score = Column(String)
    helpful_score = Column(String)
    good = Column(TEXT)
    bad = Column(TEXT)

    created_at = Column(DateTime(timezone=True), default=None)
    processed_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    apect_sum_polarity = Column(String)

    # user stats
    playtime_forever = Column(Integer)
    playtime_last_two_weeks = Column(Integer)
    playtime_at_review = Column(Integer)

    # one(game) to many(reviews)
    game = relationship("Game", back_populates="game")
    # one(user) to many(reviews)
    user = relationship("User", back_populates="user")
