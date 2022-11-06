from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Aspect(Base):
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey('review.id'))
    term = Column(String)
    category = Column(String)
    polarity = Column(String)
    confidence = Column(String)

    review = relationship("Review", back_populates="aspects")