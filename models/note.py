from datetime import datetime
from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, Integer

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=True)
    published = Column(Boolean, nullable=False, default=True)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=datetime.now())