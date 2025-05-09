'''module for testing books curd operations'''
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..crud.books import create_book, delete_book

client = TestClient(app)

TEST_BOOK = {
    "title": "Test Book",
    "author": "Test Author",
    "year": 2023
}

@pytest.fixture
def test_book():
    """fixture"""
    book = create_book(TEST_BOOK)
    yield book
    delete_book(book["book_id"])

def test_create_book():
    '''testing book creation'''
    #getting token
    auth_response = client.post(
        "/users/token",
        data={"username": "testbooks", "password": "test"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]

    test_data = {
        "title": "New Book",
        "author": "Author",
        "year": 2023
    }

    response = client.post(
        "/books/",
        json=test_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "book_id" in response_data
    assert response_data["title"] == test_data["title"]

    #existence verification
    db_book = client.get(f"/books/{response_data['book_id']}").json()
    assert db_book["book_id"] == response_data["book_id"]

def test_get_book(test_book):
    '''testing getting a book'''
    response = client.get(f"/books/{test_book['book_id']}")
    assert response.status_code == 200
    assert response.json()["book_id"] == test_book["book_id"]

def test_update_book(test_book):
    '''testing updating a book entry'''
    update_data = {"title": "Updated Title"}
    response = client.put(
        f"/books/{test_book['book_id']}",
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["book_id"] == test_book["book_id"]

def test_delete_book(test_book):
    '''testing deletion operation'''
    book_id = test_book["book_id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404
