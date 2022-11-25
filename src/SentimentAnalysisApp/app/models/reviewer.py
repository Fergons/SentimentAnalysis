from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class Reviewer(Base):
    id = Column(Integer, primary_key=True, index=True)
    source_reviewer_id = Column(String)
    source_id = Column(Integer, ForeignKey('source.id'))
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    num_reviews = Column(Integer)
    # one(user) to many(reviews)
    reviews = relationship("Review", back_populates="user", lazy="selectin")
    source = relationship("Source", back_populates="reviewers", lazy="selectin")

    