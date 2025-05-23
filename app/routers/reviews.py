'''router for the table reviews'''
from fastapi import APIRouter, Depends, HTTPException
from ..models import Review, ReviewCreate
from ..crud.reviews import get_reviews_by_book, create_review, delete_review
from ..dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review)
def create_review_route(
    review: ReviewCreate,
    current_user: dict = Depends(get_current_user)
):
    '''create review'''
    try:
        review_data = review.dict()
        review_data['user_id'] = current_user['user_id']
        return create_review(review_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/book/{book_id}", response_model=list[Review])
def read_reviews_by_book(book_id: int):
    '''get review by book id'''
    return get_reviews_by_book(book_id)

@router.delete("/{review_id}")
def delete_review_route(review_id: int):
    '''deleting an entry'''
    if not delete_review(review_id):
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
