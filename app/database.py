from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import app_settings
from app.logging_config import logger

logger.info(
    f"app_settings.SQLALCHEMY_DATABASE_URL{app_settings.SQLALCHEMY_DATABASE_URL}")

# Create the SQLAlchemy engine using the database URL from app_settings
engine = create_engine(
    app_settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


# Create a session maker object with autocommit and autoflush set to False
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

def get_db():
    """Function to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
