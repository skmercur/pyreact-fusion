"""
Tests for authentication service
"""
import pytest
from backend.services.auth import AuthService


def test_password_hashing():
    """Test password hashing and verification"""
    auth_service = AuthService()
    password = "test_password_123"
    
    # Hash password
    hashed = auth_service.get_password_hash(password)
    
    # Verify hash is different from original
    assert hashed != password
    
    # Verify password matches hash
    assert auth_service.verify_password(password, hashed) is True
    
    # Verify wrong password doesn't match
    assert auth_service.verify_password("wrong_password", hashed) is False


def test_jwt_token_creation():
    """Test JWT token creation and decoding"""
    auth_service = AuthService()
    data = {"sub": "testuser", "email": "test@example.com"}
    
    # Create token
    token = auth_service.create_access_token(data)
    
    # Verify token is created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode token
    decoded = auth_service.decode_access_token(token)
    
    # Verify decoded data
    assert decoded is not None
    assert decoded["sub"] == "testuser"
    assert decoded["email"] == "test@example.com"
    assert "exp" in decoded


def test_jwt_token_invalid():
    """Test JWT token with invalid token"""
    auth_service = AuthService()
    
    # Try to decode invalid token
    decoded = auth_service.decode_access_token("invalid_token")
    
    # Should return None
    assert decoded is None

