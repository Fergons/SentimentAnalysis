from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class Developer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    games = relationship("GameDeveloper", back_populates="developer", cascade="all, delete")
