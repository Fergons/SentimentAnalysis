"""
Created by Frantisek Sabol
"""
from sqlalchemy_utils import TSVectorType

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, TEXT, UniqueConstraint, Computed, \
    Index, and_
from sqlalchemy.orm import relationship


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    source_review_id = Column(String)  # source platform dependant
    source_reviewer_id = Column(String)
    game_id = Column(Integer, ForeignKey('game.id'))
    reviewer_id = Column(Integer, ForeignKey('reviewer.id'))
    source_id = Column(Integer, ForeignKey('source.id'))
    # url = Column(String)

    language = Column(String)
    text = Column(TEXT)
    text_tsv = Column(
        TSVectorType("text", regconfig="english"),
        Computed("to_tsvector('english', \"text\")", persisted=True))
    summary = Column(TEXT)
    score = Column(String)
    helpful_score = Column(String)
    good = Column(TEXT)
    bad = Column(TEXT)
    voted_up = Column(Boolean)

    created_at = Column(DateTime(timezone=True), default=None)
    updated_at = Column(DateTime(timezone=True), default=None)
    processed_at = Column(DateTime(timezone=True), default=None)

    aspect_sum_polarity = Column(String)

    playtime_at_review = Column(Integer)

    num_aspects = Column(Integer)
    num_positive_aspects = Column(Integer)
    num_negative_aspects = Column(Integer)

    def num_neutral_aspects(self):
        return self.num_aspects - self.num_positive_aspects - self.num_negative_aspects

    # one(game) to many(reviews)
    game = relationship("Game", back_populates="reviews")
    # one(user) to many(reviews)
    reviewer = relationship("Reviewer", back_populates="reviews")
    # one(review) to many(aspects)
    aspects = relationship("Aspect", back_populates="review", cascade="all, delete")

    analyzed_reviews = relationship("AnalyzedReview", back_populates="review")

    positive_aspects = relationship("Aspect",
                                    primaryjoin="and_(Aspect.review_id == Review.id, Aspect.polarity == 'positive')",
                                    viewonly=True)
    negative_aspects = relationship("Aspect",
                                    primaryjoin="and_(Aspect.review_id == Review.id, Aspect.polarity == 'negative')",
                                    viewonly=True)

    source = relationship("Source", back_populates="reviews")
    UniqueConstraint(source_review_id, source_id)

    __table_args__ = (
        Index("idx_review_text_tsv", text_tsv, postgresql_using="gin"),
    )
