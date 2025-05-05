'''this module establishes class structure for the app'''
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, EmailStr

class BookBase(BaseModel):
    ''''''
    title: str
    author: str
    year: int

class BookCreate(BookBase):
    ''''''
    pass

class Book(BookBase):
    ''''''
    book_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    ''''''
    username: str
    email: EmailStr

class UserCreate(UserBase):
    ''''''
    password: str

class User(UserBase):
    ''''''
    user_id: int
    disabled: bool = False
    
    class Config:
        ''''''
        orm_mode = True

class ReviewBase(BaseModel):
    ''''''
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    ''''''
    book_id: int

class Review(ReviewBase):
    ''''''
    review_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        ''''''
        orm_mode = True

class LoanBase(BaseModel):
    ''''''
    book_id: int

class LoanCreate(LoanBase):
    ''''''
    pass

class Loan(LoanBase):
    ''''''
    loan_id: int
    user_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    
    class Config:
        ''''''
        orm_mode = True

class Token(BaseModel):
    ''''''
    access_token: str
    token_type: str

class TokenData(BaseModel):
    ''''''
    username: Optional[str] = None

class UserUpdate(BaseModel):
    '''for updating user'''
    username: str | None = None
    email: str | None = None
    password: str | None = None

class BookUpdate(BaseModel):
    '''for updating books'''
    title: str | None = None
    author: str | None = None
    year: int | None = None

class LoanUpdate(BaseModel):
    '''for updating loans'''
    user_id: int | None = None
    book_id: int | None = None
    loan_date: date | None = None
    return_date: date | None = None
    due_date: date | None = None
