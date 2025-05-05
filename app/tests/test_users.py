'''testing users crud functionality'''
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

#test data
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass"
}

def test_create_user():
    '''testing user creation'''
    #creating test user
    response = client.post("/users/", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USER["username"]

    #verifying duplicate user
    response = client.post("/users/", json=TEST_USER)
    assert response.status_code == 400

def test_login():
    '''testing login'''
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
    '''testing entry update'''
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
    '''testing user deletion'''
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
