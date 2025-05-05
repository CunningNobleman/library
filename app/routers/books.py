from fastapi import APIRouter, Depends, HTTPException, status
from ..models import Book, BookCreate, BookUpdate
from ..crud.books import get_book, get_books, create_book, update_book, delete_book
from ..dependencies import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED
)
async def create_book_route(
    book: BookCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new book"""
    return create_book(book.dict())

@router.get("/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 100):
    """Get all books (public access)"""
    return get_books(skip, limit)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int):
    """Get a specific book by ID"""
    book = get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.put("/{book_id}", response_model=Book)
def update_book_route(
    book_id: int,
    book_update: BookUpdate
):
    '''updating a book entry router'''
    db_book = get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.dict(exclude_unset=True)
    updated_book = update_book(book_id, update_data)

    if not updated_book:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    return updated_book

@router.delete("/{book_id}")
def delete_book_route(book_id: int):
    '''deleting an entry router'''
    if not get_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    if not delete_book(book_id):
        raise HTTPException(status_code=400, detail="Delete failed")
    return {"message": "Book deleted successfully"}
