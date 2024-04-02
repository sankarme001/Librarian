print("Worked")
import logging
from fastapi import FastAPI
print("Worked")
# Importing from internal modules
from app import models
from app.database import engine
print("Worked")
from app.routers import users, auth, books
from app.config import app_settings
from app.settings import description
from app.logging_config import logger

print("Worked")

def initialize_app():
    """
    Initializes the FastAPI application with specified settings and routers.

    Returns:
        FastAPI: The initialized FastAPI application instance.
    """


    # Initialize FastAPI application
    app = FastAPI(
        title=app_settings.APP_NAME,
        description=description,
        version="0.0.1",
        debug=True,
        root_path="/api"
    )

    # Create database tables
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.info(f"Exception {e}")


    # Include routers for different functionalities
    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(books.router)

    # Log initialization message
    logging.info('FastAPI application initialized successfully.')

    return app
