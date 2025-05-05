'''testing reviews crud operations'''
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..database import get_db_connection

client = TestClient(app)

TEST_USER = {
    "username": "testbooks",
    "password": "test"
}

#test data
TEST_REVIEW = {
    "rating": 5,
    "comment": "Excellent book!"
}

@pytest.fixture(scope="module")
def auth_token():
    '''authorization'''
    response = client.post(
        "/users/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    return {
        "token": response.json()["access_token"],
        "user_id": 5
    }

@pytest.fixture
def test_book(auth_token):
    '''fixture'''

    response = client.post(
        "/books/",
        json={"title": "Review Test Book", "author": "Test Author", "year": 2023},
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    book = response.json()
    yield book

    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE book_id = ?", (book["book_id"],))
    conn.commit()
    conn.close()

@pytest.fixture
def test_review(auth_token, test_book):
    '''fixture'''

    review_data = {
        "book_id": test_book["book_id"],
        "rating": TEST_REVIEW["rating"],
        "comment": TEST_REVIEW["comment"]
    }
    response = client.post(
        "/reviews/",
        json=review_data,
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    review = response.json()
    yield review

    conn = get_db_connection()
    conn.execute("DELETE FROM reviews WHERE review_id = ?", (review["review_id"],))
    conn.commit()
    conn.close()

def test_create_review(auth_token, test_book):
    '''creating a review'''
    response = client.post(
        "/reviews/",
        json={
            "book_id": test_book["book_id"],
            "rating": 4,
            "comment": "Great read!"
        },
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 200
    review = response.json()
    assert "review_id" in review
    assert review["book_id"] == test_book["book_id"]
    assert review["user_id"] == 5
    assert review["rating"] == 4

def test_get_reviews_by_book(test_review, test_book):
    '''testing getting all reviews of a particular book'''
    response = client.get(f"/reviews/book/{test_book['book_id']}")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)
    assert len(reviews) > 0
    assert reviews[0]["review_id"] == test_review["review_id"]
    assert "username" in reviews[0]

def test_delete_review(auth_token, test_review):
    '''testing deletion of entries'''
    response = client.delete(
        f"/reviews/{test_review['review_id']}",
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Review deleted successfully"

    conn = get_db_connection()
    result = conn.execute(
        "SELECT 1 FROM reviews WHERE review_id = ?",
        (test_review["review_id"],)
    ).fetchone()
    conn.close()
    assert result is None

def test_create_review_invalid_book(auth_token):
    '''testing creaing a review'''
    response = client.post(
        "/reviews/",
        json={
            "book_id": 9999,
            "rating": 3,
            "comment": "Not bad"
        },
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 400
    assert "Book not found" in response.json()["detail"]
