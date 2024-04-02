import logging
from passlib.context import CryptContext
from fastapi import status, Depends, HTTPException

from app.oauth2 import get_current_user
from app.models import Users
from app.logging_config import logger

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def verify_admin_privileges(current_user: Users = Depends(get_current_user)) -> Users:
    """Verifies if the current user has admin privileges."""
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User does not have admin privileges")
        return current_user
    except Exception as e:
        logger.error(f"Error verifying admin privileges: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
