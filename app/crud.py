from fastapi import status, Response, Depends, APIRouter, HTTPException
from app import models
from sqlalchemy.orm import Session
from app.schemes import CreateUser, UserResponse, BookCreate, BookUpdate
from app.utils import hash_password
from app.database import get_db
from app.oauth2 import get_current_user
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, func, String
from app.logging_config import logger


def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = models.Books(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Books).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Books).filter(models.Books.id == book_id).first()


def update_book(db: Session, book_id: int, new_book_data: BookUpdate):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book:
        for key, value in new_book_data.model_dump().items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return book
    return None


def delete_book(db: Session, book_id: int):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False


def borrow_book(db, book_id: int, user_id: int):
    book_transaction = models.BookTransactions(
        book_id=book_id,
        borrowed_by=user_id,
        borrowed=True,
        returned=False,
        borrowed_at=datetime.now(),
        returned_at=None
    )
    db.add(book_transaction)
    db.commit()
    db.refresh(book_transaction)
    return book_transaction


def return_book(db, book_id: int):
    transaction = db.query(models.BookTransactions).filter(
        models.BookTransactions.book_id == book_id,
        models.BookTransactions.returned == False
    ).first()
    if not transaction:
        raise ValueError("Book transaction not found or already returned")

    # Update the transaction record to mark as returned
    transaction.returned = True
    transaction.returned_at = datetime.now()
    db.commit()
    db.refresh(transaction)
    return transaction

def get_books_borrowed_by_user(db: Session, user_id: int):
    return db.query(models.Books, models.BookTransactions).join(models.BookTransactions).filter(
        models.BookTransactions.borrowed_by == user_id
    ).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_user_book_history(
    db: Session,
    user_id: str = None,
    book_title: str = None,
    transaction_type: str = None,
    date: str = None
):
    # Start building the query
    query = db.query(models.Books, models.BookTransactions)

    # Apply filters based on query parameters
    if user_id:
        query = query.filter(models.BookTransactions.borrowed_by == user_id)
    if book_title:
        query = query.filter(models.Books.title == book_title)
    if transaction_type:
        if transaction_type.lower() == "borrow":
            query = query.filter(and_(models.BookTransactions.borrowed == True, models.BookTransactions.returned == False))
        else:
            query = query.filter(models.BookTransactions.returned == True)
    if date:
        query = query.filter(models.BookTransactions.borrowed_at.cast(String).like(f"%{str(date.date())}%"))

    # Execute the query and fetch the results
    user_book_history = query.all()
    return user_book_history