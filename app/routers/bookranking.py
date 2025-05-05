from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from ..database import get_db_connection
from sqlite3 import Connection



router = APIRouter(prefix="/books", tags=["books"])

class BookRanking(BaseModel):
    book_id: int
    title: str
    author: str
    year: int
    average_rating: float
    review_count: int

@router.get("/rankings", response_model=List[BookRanking])
def get_book_rankings(conn: Connection = Depends(get_db_connection)):
    """
    Get all books ranked by average review score (1-5).
    """
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                b.book_id, 
                b.title, 
                b.author, 
                b.year,
                ROUND(COALESCE(AVG(r.rating), 0), 2) AS average_rating,
                COUNT(r.review_id) AS review_count
            FROM books b
            LEFT JOIN reviews r ON b.book_id = r.book_id
            GROUP BY b.book_id
            ORDER BY average_rating DESC, review_count DESC
        ''')
        
        return [
            BookRanking(
                book_id=row['book_id'],
                title=row['title'],
                author=row['author'],
                year=row['year'],
                average_rating=row['average_rating'],
                review_count=row['review_count']
            ) 
            for row in cursor.fetchall()
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )