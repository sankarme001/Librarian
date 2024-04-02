import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException

from app import models
from app.schemes import CreateUser, UserResponse, BookBarrow, BookRead, UserBookRead
from app.utils import hash_password, verify_admin_privileges
from app.database import get_db
from app.oauth2 import get_current_user
from app.crud import (
    get_books_borrowed_by_user,
    get_user_by_email,
    get_user_book_history,
)
from sqlalchemy.orm import Session
from app.logging_config import logger

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    """Create a new user."""
    try:
        new_user = models.Users(**user.dict())
        new_user.password = hash_password(user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")


@router.get("/book")
def get_books_borrowed_by_user_api(
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get books borrowed by the current user."""
    try:
        books_borrowed = get_books_borrowed_by_user(db, current_user.id)

        if not books_borrowed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No books borrowed by this user")

        borrowed_books = []
        for book, transaction in books_borrowed:
            borrowed_books.append({
                "id": book.id,
                "title": book.title,
                "description": book.description,
                "author": book.author,
                "count": book.count,
                "borrowed_by": current_user.name,
                "borrowed": transaction.borrowed,
                "returned": transaction.returned,
                "borrowed_at": transaction.borrowed_at,
                "returned_at": transaction.returned_at
            })

        return borrowed_books

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error getting books borrowed by user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to fetch borrowed books")


@router.get("/history")
def retrieve_user_book_history_api(email: Optional[str] = None,
                                   book_title: Optional[str] = None,
                                   type_: Optional[str] = None,
                                   date: Optional[datetime] = None, current_user: models.Users = Depends(verify_admin_privileges),
                                   db: Session = Depends(get_db)
                                   ):
    """Retrieve user's book borrowing history."""
    try:
        user = get_user_by_email(db, email) if email else None

        books_history = get_user_book_history(
            db, user.id if user else None, book_title, type_, date)
        borrowed_books = []
        for book, transaction in books_history:
            borrowed_books.append({
                "id": book.id,
                "title": book.title,
                "description": book.description,
                "author": book.author,
                "count": book.count,
                "borrowed_by": transaction.borrowed_by,
                "borrowed": transaction.borrowed,
                "returned": transaction.returned,
                "borrowed_at": transaction.borrowed_at,
                "returned_at": transaction.returned_at
            })
        return borrowed_books

    except Exception as e:
        logger.error(f"Error retrieving user book history: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to fetch user book history")
