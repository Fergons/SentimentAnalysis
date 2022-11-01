from backend.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


class Aspect(Base):
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String)
    category = Column(String)
    polarity = Column(String)
    confidence = Column(String)
