from datetime import datetime
from database import Base
from sqlalchemy import Boolean, DateTime, Column, Integer, String

class UserStatus:
    Inactive = 0
    Active = 1
    Blocked = 2

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, default="")
    is_admin = Column(Boolean, default=False)
    is_active = Column(Integer, default=UserStatus.Inactive)
    created_ts = Column(DateTime, default=datetime.now)
    updated_ts = Column(DateTime, default=datetime.now, onupdate=datetime.now)