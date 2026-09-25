import pytest
from pydantic import ValidationError
import os

from models.login import LoginRequest
from models.users import UserRole
from fastapi import HTTPException

# Set environment variables before importing modules that depend on them
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing"

# Login Password validation
class TestPasswordValidation:
    """Test password validation in LoginRequest"""
    
    def test_valid_password(self):
        """Test that valid password"""
        valid_passwords = [
            "password1!",  # 8 chars, has digit, has special char
            "Password123!",  # longer password with uppercase
            "test@1234",  # exactly 8 chars
        ]
        
        for password in valid_passwords:
            request = LoginRequest(
                email="test@example.com",
                password=password
            )
            assert request.password == password
    
    def test_password_too_short(self):
        """Test that password shorter than 8 chars fails validation"""
        short_passwords = [
            "pass1!",  # 6 chars
            "pwd1",  # 4 chars
            "p1!",  # 3 chars
        ]
        
        for password in short_passwords:
            with pytest.raises(ValidationError) as exc_info:
                LoginRequest(
                    email="test@example.com",
                    password=password
                )
            assert "Password must be between 8-12 chars" in str(exc_info.value)
    
    def test_password_without_digit(self):
        """Test that password without digit"""
        passwords_without_digit = [
            "password!",  # no digit
            "Test!@#$%",  # no digit, but long enough
        ]
        
        for password in passwords_without_digit:
            with pytest.raises(ValidationError) as exc_info:
                LoginRequest(
                    email="test@example.com",
                    password=password
                )
            assert "Password must contain at least one digit" in str(exc_info.value)
    
    def test_password_without_special_char(self):
        """Test that password without special character"""
        passwords_without_special = [
            "password1",  # no special char
            "Test12345",  # no special char
        ]
        
        for password in passwords_without_special:
            with pytest.raises(ValidationError) as exc_info:
                LoginRequest(
                    email="test@example.com",
                    password=password
                )
            assert "Password must contain at least one special character" in str(exc_info.value)

# User role validation
class TestAdminRole:
    """Test admin role requirement in authentication middleware"""
    
    def test_admin_user(self):
        """Test that admin user passes require_admin check"""
        admin_user = {
            "user_id": "12345",
            "email": "admin@example.com",
            "role": UserRole.ADMIN.value
        }
        
        # Use the extracted check_admin_role function for testing
        from middleware.auth import check_admin_role
        
        result = check_admin_role(admin_user)
        assert result == admin_user
        assert result["role"] == UserRole.ADMIN.value
    
    def test_non_admin_user(self):
        """Test that non-admin user raises 403 Forbidden"""
        regular_user = {
            "user_id": "12345",
            "email": "user@example.com",
            "role": UserRole.USER.value
        }
        
        from middleware.auth import check_admin_role
        
        with pytest.raises(HTTPException) as exc_info:
            check_admin_role(regular_user)
        
        assert exc_info.value.status_code == 403
        assert "Admin access required" in exc_info.value.detail