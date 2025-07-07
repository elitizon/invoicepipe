"""{{cookiecutter.project_name}} FastAPI application.

This module provides a simple Hello World FastAPI application.
The application includes basic endpoints for greeting users and health checks.

Example:
    To run this application:

    >>> from {{cookiecutter.package_name}}.main import app
    >>> # Use with uvicorn: uvicorn {{cookiecutter.package_name}}.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

from .config import settings

__all__ = ["app"]


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str
    name: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str


def create_app() -> FastAPI:
    """Factory to create the FastAPI application."""
    app = FastAPI(
        title="{{cookiecutter.project_name}}",
        description="{{cookiecutter.description}}",
        version=settings.version,
    )
    
    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint that returns a simple greeting."""
        return {"message": "Hello World!"}
    
    @app.get("/hello/{name}", response_model=HelloResponse)
    async def hello(name: str) -> HelloResponse:
        """Personalized hello endpoint."""
        return HelloResponse(
            message=f"Hello, {name}!",
            name=name
        )
    
    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            version=settings.version
        )
    
    return app


app = create_app()
