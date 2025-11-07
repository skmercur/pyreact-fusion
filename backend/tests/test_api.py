"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "environment" in data
    assert "database" in data


def test_register_user():
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    
    # Should succeed or fail with 400 if user already exists
    assert response.status_code in [201, 400]
    
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]


def test_login():
    """Test user login"""
    # First register a user
    user_data = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "testpassword123",
    }
    
    # Register
    client.post("/api/auth/register", json=user_data)
    
    # Login
    response = client.post(
        "/api/auth/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )
    
    # Should succeed
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_protected_endpoint():
    """Test protected endpoint without authentication"""
    response = client.get("/api/users")
    
    # Should fail with 401 Unauthorized
    assert response.status_code == 401


def test_protected_endpoint_with_token():
    """Test protected endpoint with valid token"""
    # Register and login
    user_data = {
        "username": "protectedtest",
        "email": "protectedtest@example.com",
        "password": "testpassword123",
    }
    
    client.post("/api/auth/register", json=user_data)
    
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Should succeed
    assert response.status_code == 200
    assert isinstance(response.json(), list)

