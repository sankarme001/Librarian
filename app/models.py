from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, TIMESTAMP, text, DateTime, Enum, ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base


class Users(Base):
    """Class representing the 'users' table in the database."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum("admin", "user", name="user_roles"), default="user")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        default=text('now()'), onupdate=text('now()'))


class Books(Base):
    """Class representing the 'books' table in the database."""

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)
    author = Column(String, unique=True, nullable=False)
    count = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        default=text('now()'), onupdate=text('now()'))


class BookTransactions(Base):
    """Class representing the 'book_transactions' table in the database."""

    __tablename__ = 'book_transactions'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrowed_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    borrowed = Column(Boolean, default=True)
    returned = Column(Boolean, default=False)
    borrowed_at = Column(TIMESTAMP(timezone=True),
                         nullable=False, server_default=text('now()'))
    returned_at = Column(TIMESTAMP(timezone=True))

    user = relationship("Users", backref="book_transactions")
    book = relationship("Books", backref="book_transactions")
