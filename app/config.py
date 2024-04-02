from typing import Optional
from dotenv import load_dotenv
import logging

from pydantic_settings import BaseSettings
from app.logging_config import logger

# Load environment variables from .env file
load_dotenv()


class AppSettings(BaseSettings):
    """Settings for the application."""
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHIM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    APP_NAME: str = "LIBRARIAN"

    class Config:
        """Configuration settings."""
        # Specify the .env file for environment variables
        env_file = ".env"


# Create an instance of AppSettings
app_settings = AppSettings()

# Example logging
logger.info("App settings loaded successfully.")
