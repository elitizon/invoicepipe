"""Tests for utility functions."""

import pytest

from {{cookiecutter.package_name}}.tools import (
    create_greeting,
    format_response,
    get_app_info,
    validate_name,
)


class TestGreetingFunctions:
    """Test cases for greeting functions."""

    def test_create_greeting_with_name(self) -> None:
        """Test creating a greeting with a name."""
        result = create_greeting("Alice")
        assert result == "Hello, Alice!"

    def test_create_greeting_with_custom_type(self) -> None:
        """Test creating a greeting with custom greeting type."""
        result = create_greeting("Bob", "Hi")
        assert result == "Hi, Bob!"

    def test_create_greeting_empty_name(self) -> None:
        """Test creating a greeting with empty name."""
        result = create_greeting("")
        assert result == "Hello, World!"

    def test_create_greeting_whitespace_name(self) -> None:
        """Test creating a greeting with whitespace-only name."""
        result = create_greeting("   ")
        assert result == "Hello, World!"

    def test_create_greeting_long_name(self) -> None:
        """Test creating a greeting with a very long name."""
        long_name = "A" * 100
        result = create_greeting(long_name)
        # Should be trimmed to 50 characters
        assert result == f"Hello, {'A' * 50}!"


class TestResponseFormatting:
    """Test cases for response formatting."""

    def test_format_response_success(self) -> None:
        """Test formatting a successful response."""
        result = format_response("Operation completed")
        expected = {"success": True, "message": "Operation completed"}
        assert result == expected

    def test_format_response_failure(self) -> None:
        """Test formatting a failed response."""
        result = format_response("Operation failed", success=False)
        expected = {"success": False, "message": "Operation failed"}
        assert result == expected


class TestNameValidation:
    """Test cases for name validation."""

    def test_validate_name_valid(self) -> None:
        """Test validating valid names."""
        assert validate_name("Alice") is True
        assert validate_name("Bob Smith") is True
        assert validate_name("Jean-Pierre") is True
        assert validate_name("O'Connor") is True

    def test_validate_name_invalid(self) -> None:
        """Test validating invalid names."""
        assert validate_name("") is False
        assert validate_name("   ") is False
        assert validate_name("Alice123") is False
        assert validate_name("Bob@Smith") is False

    def test_validate_name_non_string(self) -> None:
        """Test validating non-string inputs."""
        assert validate_name(123) is False  # type: ignore
        assert validate_name(None) is False  # type: ignore
        assert validate_name([]) is False  # type: ignore


class TestAppInfo:
    """Test cases for app information."""

    def test_get_app_info(self) -> None:
        """Test getting app information."""
        result = get_app_info()
        
        assert isinstance(result, dict)
        assert "message" in result
        assert "description" in result
        assert "endpoints" in result
        assert result["message"] == "Welcome to the Hello World API!"
        assert "FastAPI" in result["description"]
        assert "GET /" in result["endpoints"]
