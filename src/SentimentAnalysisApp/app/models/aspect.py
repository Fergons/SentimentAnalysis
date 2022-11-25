from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class Aspect(Base):
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey('review.id'))
    term = Column(String)
    category = Column(String)
    polarity = Column(String)
    confidence = Column(String)
    #ML model that was used to analyse review
    model_id = Column(String)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())

    review = relationship("Review", back_populates="aspects", lazy="selectin")