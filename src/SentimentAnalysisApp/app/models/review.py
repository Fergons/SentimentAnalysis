from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, TEXT
from sqlalchemy.orm import relationship


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    source_review_id = Column(Integer)  # source platform dependant
    game_id = Column(Integer, ForeignKey('game.id'))
    user_id = Column(Integer, ForeignKey('reviewer.id'))
    source_id = Column(String, ForeignKey('source.id'))

    language = Column(String)
    text = Column(TEXT)
    summary = Column(TEXT)
    score = Column(String)
    helpful_score = Column(String)
    good = Column(TEXT)
    bad = Column(TEXT)
    voted_up = Column(Boolean)

    created_at = Column(DateTime(timezone=True), default=None)
    processed_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    apect_sum_polarity = Column(String)

    # user stats
    playtime_forever = Column(Integer)
    playtime_last_two_weeks = Column(Integer)
    playtime_at_review = Column(Integer)

    # one(game) to many(reviews)
    game = relationship("Game", back_populates="reviews")
    # one(user) to many(reviews)
    user = relationship("Reviewer", back_populates="reviews")
    # one(review) to many(aspects)
    aspects = relationship("Aspect", back_populates="review")

    source = relationship("Source", back_populates="reviews")
