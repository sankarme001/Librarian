from datetime import datetime, timedelta
import logging

from fastapi import (
    APIRouter, Depends, HTTPException, Response, status
)
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.config import app_settings
from app.database import get_db
from app.schemes import TokenData
from app.logging_config import logger

# Create an OAuth2 password bearer schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# Retrieve settings from app_settings
SECRET_KEY = app_settings.SECRET_KEY
ALGORITHIM = app_settings.ALGORITHIM
ACCESS_TOKEN_EXPIRE_MINUTES = app_settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict) -> str:
    """Generate an access token based on input data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%dT%H:%M:%SZ")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHIM)


def verify_access_token(token: str, credentials_exception) -> TokenData:
    """Verify the access token and return token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = TokenData(id=user_id)
        logger.info(f"Token verified successfully for user ID: {user_id}")
    except JWTError:
        logger.error("Error decoding JWT token")
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)) -> models.Users:
    """Get the current user based on the access token."""
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        token_data = verify_access_token(token, credentials_exception)
        user = db.query(models.Users).filter(
            models.Users.id == token_data.id).first()
        if not user:
            logger.warning(f"User not found with ID: {token_data.id}")
            raise credentials_exception
        logger.info(f"Current user retrieved: {user.name}")
        return user
    except Exception as e:
        logger.error(f"Error while getting current user: {e}")
        raise credentials_exception
