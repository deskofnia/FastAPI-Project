from datetime import datetime
from database import Base
from sqlalchemy import Boolean, DateTime, Column, Integer, String

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_ts = Column(DateTime, default=datetime.now)
    updated_ts = Column(DateTime, default=datetime.now, onupdate=datetime.now)