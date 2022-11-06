from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


# class Source(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String)
#     updated_at = Column(DateTime(timezone=True), default=None, onupdate=func.now())
#
#     # one(user) to many(reviews)
#     reviews = relationship("Review", back_populates="review")
#     reviewers = relationship("Reviewers", back_populates="source")
