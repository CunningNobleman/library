from fastapi import APIRouter, Depends, HTTPException
from ..models import Review, ReviewCreate
from ..crud.reviews import get_reviews_by_book, create_review
from ..dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review)
def create_review_route(
    review: ReviewCreate,
    current_user: dict = Depends(get_current_user)
):
    try:
        review_data = review.dict()
        review_data['user_id'] = current_user['user_id']
        return create_review(review_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/book/{book_id}", response_model=list[Review])
def read_reviews_by_book(book_id: int):
    return get_reviews_by_book(book_id)