from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

#test data
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass"
}

def test_create_user():
    #creating test user
    response = client.post("/users/", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USER["username"]
    
    #verifying duplicate user
    response = client.post("/users/", json=TEST_USER)
    assert response.status_code == 400

def test_login():
    #getting token
    response = client.post(
        "/users/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    #invalid login
    response = client.post(
        "/users/token",
        data={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401

def test_update_user():
    #signing in to get token
    auth = client.post(
        "/users/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    token = auth.json()["access_token"]
    
    #updating user
    update_data = {"email": "new@example.com"}
    response = client.put(
        f"/users/{TEST_USER['username']}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"

def test_delete_user():
    #login
    auth = client.post(
        "/users/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    token = auth.json()["access_token"]
    
    # Delete user
    response = client.delete(
        f"/users/{TEST_USER['username']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    
    #verification
    response = client.post(
        "/users/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    assert response.status_code == 401


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
        data={"username": "testuser", "password": "testpass"}
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
    """Test deleting book (public)"""
    response = client.delete(f"/books/{test_book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
    
    # Verify deletion
    response = client.get(f"/books/{test_book_id}")
    assert response.status_code == 404