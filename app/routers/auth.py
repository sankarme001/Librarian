from typing import List  

from fastapi import status, Response, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session  
from app import models  
from app.schemes import CreateUser, UserResponse, UserLogin, Token
from app.utils import verify_password
from app.database import get_db
from app.oauth2 import create_access_token
from app.logging_config import logger

router = APIRouter(prefix="/auth", tags=["authendication"])


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info("Login request received")  # Log the start of the login request
    
    try:
        user = db.query(models.Users).filter(
            models.Users.email == user_credentials.username).first()
        if not user:
            logger.warning("User not found")  # Log a warning if the user is not found
            raise HTTPException(detail="Invalid Credentials", status_code=status.HTTP_403_FORBIDDEN)
        
        if not verify_password(user_credentials.password, user.password):
            logger.warning("Invalid password")  # Log a warning for invalid password
            raise HTTPException(detail="Invalid Credentials", status_code=status.HTTP_403_FORBIDDEN)

        access_token = create_access_token({"user_id": user.id})
        logger.info("Login successful")  # Log a success message for successful login
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc}")  # Log HTTP exceptions
        raise http_exc
    
    except Exception as e:
        logger.error(f"Exception: {e}")  # Log other unexpected exceptions
        raise HTTPException(detail="Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)