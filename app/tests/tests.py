from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


#test data for books
TEST_BOOK = {
    "title": "Test Book",
    "author": "Test Author",
    "description": "This is a test book",
    "year": 2023
}


test_book_id = None

def test_create_book():
    """Test book creation"""
    auth = client.post(
        "/users/token",
        data={"username": "testbooks", "password": "test"}
    )
    token = auth.json()["access_token"]
    
    #create book
    response = client.post(
        "/books/",
        json=TEST_BOOK,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == TEST_BOOK["title"]
    global test_book_id
    test_book_id = response.json()["id"]

def test_get_books():
    """Test getting all books"""
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_book():
    """Test getting specific book (public)"""
    response = client.get(f"/books/{test_book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_book_id

def test_update_book():
    """Test updating book"""
    update_data = {"title": "Updated Title"}
    response = client.put(
        f"/books/{test_book_id}",
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_book():
    """Test deleting book"""
    response = client.delete(f"/books/{test_book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
    
    #verify
    response = client.get(f"/books/{test_book_id}")
    assert response.status_code == 404

#loan test data
TEST_LOAN = {
    "book_id": 1,
    "loan_date": "2023-01-01",
    "due_date": "2023-02-01"
}

#same for review
TEST_REVIEW = {
    "book_id": 1,
    "rating": 5,
    "comment": "Excellent book!"
}

test_loan_id = None
test_review_id = None

def test_create_loan():
    """Test loan creation"""
    global test_loan_id
    
    auth = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = auth.json()["access_token"]
    
    # Create loan
    response = client.post(
        "/loans/",
        json=TEST_LOAN,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    test_loan_id = response.json()["loan_id"]

def test_get_user_loans():
    """Test getting user's loans"""
    auth = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = auth.json()["access_token"]
    
    response = client.get(
        "/loans/my-loans",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_loan():
    """Test updating loan"""
    update_data = {"due_date": "2023-03-01"}
    response = client.put(
        f"/loans/{test_loan_id}",
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["due_date"] == "2023-03-01"

def test_delete_loan():
    """Test deleting loan"""
    response = client.delete(f"/loans/{test_loan_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Loan deleted successfully"

def test_create_review():
    """Test review creation"""
    global test_review_id
    
    # Get auth token
    auth = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = auth.json()["access_token"]
    
    # Create review
    response = client.post(
        "/reviews/",
        json=TEST_REVIEW,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    test_review_id = response.json()["review_id"]

def test_get_reviews_by_book():
    """Test getting reviews for a book"""
    response = client.get(f"/reviews/book/{TEST_REVIEW['book_id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_delete_review():
    """Test deleting review"""
    response = client.delete(f"/reviews/{test_review_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Review deleted successfully"