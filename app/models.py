from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    book_id: int
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    disabled: bool = False
    
    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    book_id: int

class Review(ReviewBase):
    review_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class LoanBase(BaseModel):
    book_id: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    loan_id: int
    user_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True