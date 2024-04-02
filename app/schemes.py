from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    """Model for creating a new user."""
    name: str
    email: EmailStr
    password: str
    is_active: bool = True
    role: str = "user"

class UserResponse(BaseModel):
    """Model for user response."""
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        """Configuration for UserResponse."""
        from_attributes = True

class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Model for authentication token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Model for token data."""
    id: Optional[int] = None

class BookBase(BaseModel):
    """Base model for books."""
    title: str
    description: str
    author: str
    count: int

class BookCreate(BookBase):
    """Model for creating a new book."""
    pass

class Book(BookBase):
    """Model for book details."""
    id: int

class PaginatedBooks(BaseModel):
    """Model for paginated books."""
    total: int
    items: List[Book]

class BookUpdate(BaseModel):
    """Model for updating a book."""
    title: str
    description: str
    author: str
    count: int

class BookDelete(BaseModel):
    """Model for deleting a book."""
    pass

class BookRead(BaseModel):
    """Model for reading book details."""
    id: int
    title: str
    description: str
    author: str
    count: int

    class Config:
        """Configuration for BookRead."""
        from_attributes = True

class BookBarrow(BaseModel):
    """Model for book borrowing."""
    id: int
    book_id: int
    borrowed_by: int
    borrowed: bool
    returned: bool
    borrowed_at: Optional[datetime]
    returned_at: Optional[datetime]

    class Config:
        """Configuration for BookBarrow."""
        from_attributes = True

class BorrowedBookRead(BaseModel):
    """Model for reading borrowed book details."""
    book: BookRead
    borrowed_book: BookBarrow

class UserBookRead(BaseModel):
    """Model for reading user book details."""
    id: int
    title: str
    description: str
    author: str
    count: str
    borrowed_by: str
    borrowed: bool
    returned: bool
    borrowed_at: Optional[datetime]
    returned_at: Optional[datetime]

    class Config:
        """Configuration for UserBookRead."""
        from_attributes = True