import logging
from datetime import datetime
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app import models
from app.crud import (
    add_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book,
    borrow_book,
    return_book,
)
from app.database import get_db
from app.models import Users
from app.schemes import (
    CreateUser,
    UserResponse,
    BookCreate,
    Book,
    PaginatedBooks,
    BookUpdate,
    BookRead,
    BorrowedBookRead,
    BookBarrow,
)
from app.utils import verify_admin_privileges
from app.oauth2 import get_current_user
from app.logging_config import logger


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: Users = Depends(verify_admin_privileges)):
    """Create a new book."""
    try:
        return add_book(db=db, book=book)
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add book")


@router.get("/", response_model=PaginatedBooks)
def get_books(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
):
    """Get paginated list of books."""
    try:
        books = get_all_books(db, skip=(page - 1) * page_size, limit=page_size)
        total_books = db.query(models.Books).count()
        return {"total": total_books, "items": books}
    except Exception as e:
        logger.error(f"Error getting books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch books")


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a book by ID."""
    book = get_book_by_id(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookUpdate)
def update_book_endpoint(
    book_id: int, book_data: BookUpdate, db: Session = Depends(get_db), current_user: Users = Depends(verify_admin_privileges)
):
    """Update a book by ID."""
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    updated_book = update_book(db, book=book, new_book_data=book_data)
    return updated_book


@router.delete("/{book_id}")
def delete_book_endpoint(
    book_id: int, db: Session = Depends(get_db), current_user: Users = Depends(verify_admin_privileges)
):
    """Delete a book by ID."""
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    delete_book(db, book)
    return {"message": "Book deleted successfully"}


@router.post("/{book_id}/borrow", response_model=BorrowedBookRead)
def borrow_book_endpoint(
    book_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)
):
    """Borrow a book."""
    try:
        book = get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        if book.count <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Book is not available for borrowing")
        borrowed_book = borrow_book(db, book_id, current_user.id)
        return BorrowedBookRead(book=book, borrowed_book=borrowed_book)
    except Exception as e:
        logger.error(f"Error borrowing book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to borrow book")


@router.put("/{book_id}/return", response_model=BorrowedBookRead)
def return_book_endpoint(
    book_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)
):
    """Return a borrowed book."""
    try:
        book = get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        returned_book = return_book(db, book.id)
        return BorrowedBookRead(book=book, borrowed_book=returned_book)
    except Exception as e:
        logger.error(f"Error returning book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to return book")
