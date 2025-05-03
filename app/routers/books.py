from fastapi import APIRouter, Depends, HTTPException
from ..models import Book, BookCreate
from ..crud.books import get_book, get_books, create_book
from ..dependencies import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
def create_book_route(book: BookCreate, current_user: dict = Depends(get_current_user)):
    return create_book(book.dict())

@router.get("/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 100):
    return get_books(skip, limit)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int):
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book