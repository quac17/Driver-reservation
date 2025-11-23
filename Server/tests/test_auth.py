import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test Data
USER_CREDENTIALS = {"username": "user1", "password": "123456"}
MENTOR_CREDENTIALS = {"username": "mentor1", "password": "123456"}
INVALID_PASSWORD = {"username": "user1", "password": "wrongpassword"}
INVALID_USER = {"username": "nonexistent", "password": "123"}

def test_login_user_success():
    """AUTH-01: Successful authentication for a standard user"""
    response = client.post("/authen/login", data=USER_CREDENTIALS)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["message"]["loginData"]["username"] == USER_CREDENTIALS["username"]
    assert data["message"]["loginData"]["isMentor"] is False

def test_login_mentor_success():
    """AUTH-02: Successful authentication for a mentor"""
    response = client.post("/authen/login", data=MENTOR_CREDENTIALS)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["message"]["loginData"]["username"] == MENTOR_CREDENTIALS["username"]
    assert data["message"]["loginData"]["isMentor"] is True

def test_login_fail_wrong_password():
    """AUTH-03: Failed authentication due to incorrect password"""
    response = client.post("/authen/login", data=INVALID_PASSWORD)
    assert response.status_code == 400
    assert response.json()["detail"] == "Sai tên đăng nhập hoặc mật khẩu"

def test_login_fail_user_not_found():
    """AUTH-04: Failed authentication because the username does not exist"""
    response = client.post("/authen/login", data=INVALID_USER)
    assert response.status_code == 400
    assert response.json()["detail"] == "Sai tên đăng nhập hoặc mật khẩu"

def test_access_protected_resource_valid_token():
    """AUTH-05: Accessing an authenticated resource with a valid JWT Token"""
    # Login first to get token
    login_res = client.post("/authen/login", data=USER_CREDENTIALS)
    token = login_res.json()["access_token"]
    
    # Access protected resource (using get user by id as example, assuming user1 has id 1)
    # We need to find the user id first or use an endpoint that uses current_user directly if available.
    # /user/me is not available, but /user/{id} is. 
    # Let's assume user1 has ID 1 based on init.sql usually starting sequences at 1.
    # Alternatively, we can use the login response to get ID if available, but it's not in the minimal response shown in code.
    # However, the login response has `loginData` which might not have ID.
    # Let's try to get user 1.
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/1", headers=headers)
    
    # If user 1 exists and token is valid, it should be 200. 
    # If user 1 is not user1, it might be 403, but still authenticated.
    # If 401, then auth failed.
    assert response.status_code in [200, 403, 404] 
    assert response.status_code != 401

def test_access_protected_resource_invalid_token():
    """AUTH-06: Accessing an authenticated resource with an expired or invalid JWT Token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/user/1", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_logout_success():
    """AUTH-07: Successful logout and Token invalidation"""
    # Login
    login_res = client.post("/authen/login", data=USER_CREDENTIALS)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Logout
    logout_res = client.post("/authen/logout", headers=headers)
    assert logout_res.status_code == 200
    assert logout_res.json()["msg"] == "Logout thành công. Token đã được invalidate."
    
    # Try to access protected resource with invalidated token
    access_res = client.get("/user/1", headers=headers)
    assert access_res.status_code == 401
