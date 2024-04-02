import logging

from app import initialize_app
from app.logging_config import logger

# Initialize FastAPI app
app = initialize_app()


@app.get("/")
async def root():
    """Root endpoint to check if the backend is up and running."""
    try:
        return "Librarian App Backend Up and Running"
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        return {"error": "Internal Server Error"}
