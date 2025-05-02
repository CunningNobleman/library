from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .dependencies import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=models.Book)
def create_book(book: models.BookCreate, db: Session = Depends(get_db)):
    db_book = schemas.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=list[models.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(schemas.Book).offset(skip).limit(limit).all()

@router.get("/{book_id}", response_model=models.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(schemas.Book).filter(schemas.Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book