from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = f"{settings.db}://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
