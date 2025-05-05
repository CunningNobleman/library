import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from ..main import app
from ..database import get_db_connection

client = TestClient(app)

# Existing test user credentials (user_id=5 in your db)
TEST_USER = {
    "username": "testbooks",
    "password": "test"
}

@pytest.fixture(scope="module")
def auth_token():
    # Only get token for existing user - NO USER CREATION
    response = client.post(
        "/users/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    return {
        "token": response.json()["access_token"],
        "user_id": 5  # Hardcoded to your existing test user
    }

@pytest.fixture
def test_book(auth_token):
    # Create test book
    response = client.post(
        "/books/",
        json={"title": "Loan Test Book", "author": "Test", "year": 2023},
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    book = response.json()
    yield book
    # Cleanup via direct DB access
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE book_id = ?", (book["book_id"],))
    conn.commit()
    conn.close()

@pytest.fixture
def test_loan(auth_token, test_book):
    # Create test loan
    response = client.post(
        "/loans/",
        json={"book_id": test_book["book_id"]},
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    loan = response.json()
    yield loan
    # Cleanup via direct DB access
    conn = get_db_connection()
    conn.execute("DELETE FROM book_loans WHERE loan_id = ?", (loan["loan_id"],))
    conn.commit()
    conn.close()

def test_create_loan(auth_token, test_book):
    response = client.post(
        "/loans/",
        json={"book_id": test_book["book_id"]},
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 200
    loan = response.json()
    assert "loan_id" in loan
    assert loan["book_id"] == test_book["book_id"]
    assert loan["user_id"] == 5  # Your existing test user ID

def test_get_user_loans(auth_token, test_loan):
    response = client.get(
        "/loans/my-loans",
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 200
    loans = response.json()
    assert isinstance(loans, list)
    assert any(loan["loan_id"] == test_loan["loan_id"] for loan in loans)

def test_update_loan(auth_token, test_loan):
    new_due_date = (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d")
    response = client.put(
        f"/loans/{test_loan['loan_id']}",
        json={"due_date": new_due_date},
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 200
    assert response.json()["due_date"] == new_due_date

def test_delete_loan(auth_token, test_loan):
    response = client.delete(
        f"/loans/{test_loan['loan_id']}",
        headers={"Authorization": f"Bearer {auth_token['token']}"}
    )
    assert response.status_code == 200
    # Verify deletion
    conn = get_db_connection()
    result = conn.execute(
        "SELECT 1 FROM book_loans WHERE loan_id = ?", 
        (test_loan["loan_id"],)
    ).fetchone()
    conn.close()
    assert result is None