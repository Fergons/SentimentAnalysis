from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, TEXT, UniqueConstraint
from sqlalchemy.orm import relationship


class AnalyzedReview(Base):
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey('review.id'))
    cleaned_text = Column(TEXT)
    task = Column(String)
    model = Column(String)
    prediction = Column(String)
    gold_label = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    review = relationship("Review", back_populates="analyzed_reviews")
    analyzed_review_sentences = relationship("AnalyzedReviewSentence", back_populates="analyzed_review")

    UniqueConstraint(review_id, model, task)

class AnalyzedReviewSentence(Base):
    id = Column(Integer, primary_key=True, index=True)
    analyzed_review_id = Column(Integer, ForeignKey('analyzedreview.id'))
    sentence = Column(TEXT)
    prediction = Column(String)
    gold_label = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    analyzed_review = relationship("AnalyzedReview", back_populates="analyzed_review_sentences")