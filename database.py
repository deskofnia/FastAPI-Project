from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import env_variables

# SQLITE_DATABASE_URL = "sqlite:///./note.db"
# connect_args={"check_same_thread": False}

engine = create_engine(
    env_variables.SQLALCHEMY_DATABASE_URI, echo=True, 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

