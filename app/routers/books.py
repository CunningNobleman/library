from fastapi import APIRouter, Depends, HTTPException, status
from ..models import Book, BookCreate
from ..crud.books import get_book, get_books, create_book
from ..dependencies import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.post(
    "/", 
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)]
)
def create_book_route(book: BookCreate):
    """Create a new book"""
    return create_book(book.dict())

@router.get("/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 100):
    """Get all books"""
    return get_books(skip, limit)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int):
    """Get a specific book by ID (public access)"""
    book = get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book