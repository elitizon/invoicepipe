"""Integration tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from {{cookiecutter.package_name}}.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints."""

    def test_root_endpoint(self) -> None:
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World!"}

    def test_hello_endpoint(self) -> None:
        """Test the hello endpoint with a name."""
        response = client.get("/hello/Alice")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, Alice!"
        assert data["name"] == "Alice"

    def test_hello_endpoint_with_special_characters(self) -> None:
        """Test the hello endpoint with special characters."""
        response = client.get("/hello/Jean-Pierre")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, Jean-Pierre!"
        assert data["name"] == "Jean-Pierre"

    def test_health_endpoint(self) -> None:
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_nonexistent_endpoint(self) -> None:
        """Test that nonexistent endpoints return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404


class TestAPIResponseModels:
    """Test cases for API response models."""

    def test_hello_response_structure(self) -> None:
        """Test that hello response has correct structure."""
        response = client.get("/hello/TestUser")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "message" in data
        assert "name" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)

    def test_health_response_structure(self) -> None:
        """Test that health response has correct structure."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "version" in data
        assert isinstance(data["status"], str)
        assert isinstance(data["version"], str)
