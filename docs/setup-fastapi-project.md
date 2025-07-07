# Setting Up a FastAPI Project with Modern Python Tooling

This guide walks you through setting up a FastAPI project using the modern Python toolset described in the [InvoicePipe specification](spec-invoice.md), including UV, Ruff, Hatchling, and other contemporary tools.

## Prerequisites

- Python 3.11+ installed
- Basic understanding of Python and web APIs
- Git for version control

## 1. Install UV (Universal Python Package Manager)

UV is a next-generation Python package installer and resolver that's much faster than pip.

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv

# Verify installation
uv --version
```

## 2. Project Setup

### 2.1 Create Project Structure

```bash
# Create project directory
mkdir my-fastapi-project
cd my-fastapi-project

# Initialize git repository
git init

# Create virtual environment with UV
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 2.2 Create pyproject.toml

Create a `pyproject.toml` file with modern Python project configuration:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-fastapi-project"
dynamic = ["version"]
description = "FastAPI project with modern Python tooling"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "python-multipart>=0.0.6",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/my-fastapi-project"
Repository = "https://github.com/yourusername/my-fastapi-project"
Issues = "https://github.com/yourusername/my-fastapi-project/issues"

[project.scripts]
my-app = "my_fastapi_project.cli.main:main"

[tool.hatch.version]
path = "src/my_fastapi_project/__init__.py"

[tool.ruff]
line-length = 88
target-version = "py311"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-string-normalization = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## 3. Install Dependencies

```bash
# Install all dependencies including dev dependencies
uv pip install -e ".[dev]"

# Or install just the main dependencies
uv pip install -e .
```

## 4. Create Project Structure

```bash
# Create source directory structure
mkdir -p src/my_fastapi_project/{api,cli,core,models,utils}
mkdir -p src/my_fastapi_project/api/{routes,middleware}
mkdir -p src/my_fastapi_project/cli/commands
mkdir -p tests

# Create __init__.py files
touch src/my_fastapi_project/__init__.py
touch src/my_fastapi_project/api/__init__.py
touch src/my_fastapi_project/api/routes/__init__.py
touch src/my_fastapi_project/api/middleware/__init__.py
touch src/my_fastapi_project/cli/__init__.py
touch src/my_fastapi_project/cli/commands/__init__.py
touch src/my_fastapi_project/core/__init__.py
touch src/my_fastapi_project/models/__init__.py
touch src/my_fastapi_project/utils/__init__.py
touch tests/__init__.py
```

## 5. Create Core Files

### 5.1 Version File

Create `src/my_fastapi_project/__init__.py`:

```python
"""My FastAPI Project - Modern Python web API."""

__version__ = "0.1.0"
```

### 5.2 FastAPI Application

Create `src/my_fastapi_project/api/main.py`:

```python
"""FastAPI application factory and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from my_fastapi_project.api.routes import health
from my_fastapi_project.core.config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix=settings.API_V1_STR)

    return app


app = create_app()
```

### 5.3 Configuration

Create `src/my_fastapi_project/core/config.py`:

```python
"""Application configuration settings."""

import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "My FastAPI Project"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "FastAPI project with modern Python tooling"
    API_V1_STR: str = "/api/v1"
    
    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### 5.4 Health Check Route

Create `src/my_fastapi_project/api/routes/health.py`:

```python
"""Health check endpoints."""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter

from my_fastapi_project.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/info")
async def app_info() -> Dict[str, Any]:
    """Application information endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "environment": settings.ENVIRONMENT,
    }
```

### 5.5 Pydantic Models

Create `src/my_fastapi_project/models/base.py`:

```python
"""Base Pydantic models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response model."""

    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: Optional[str] = None


class ErrorResponse(BaseResponse):
    """Error response model."""

    success: bool = False
    error_code: str
    error_message: str
    details: Optional[dict] = None
```

### 5.6 CLI Interface

Create `src/my_fastapi_project/cli/main.py`:

```python
"""Command line interface."""

import click
import uvicorn

from my_fastapi_project.core.config import settings


@click.group()
@click.version_option(version=settings.VERSION)
def main():
    """My FastAPI Project CLI."""
    pass


@main.command()
@click.option("--host", default=settings.HOST, help="Host address")
@click.option("--port", default=settings.PORT, help="Port number")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
@click.option("--workers", default=1, help="Number of workers")
def serve(host: str, port: int, reload: bool, workers: int):
    """Start the FastAPI server."""
    uvicorn.run(
        "my_fastapi_project.api.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
    )


if __name__ == "__main__":
    main()
```

## 6. Create Tests

### 6.1 Test Configuration

Create `tests/conftest.py`:

```python
"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from my_fastapi_project.api.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)
```

### 6.2 API Tests

Create `tests/test_api.py`:

```python
"""API endpoint tests."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_app_info(client: TestClient):
    """Test app info endpoint."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data
```

## 7. Development Tools Setup

### 7.1 Create Development Scripts

Create `scripts/dev.py`:

```python
"""Development helper scripts."""

import subprocess
import sys


def run_command(command: str) -> int:
    """Run a shell command."""
    print(f"Running: {command}")
    return subprocess.run(command, shell=True).returncode


def lint():
    """Run linting."""
    return run_command("ruff check src/ tests/")


def format_code():
    """Format code."""
    return run_command("ruff format src/ tests/")


def test():
    """Run tests."""
    return run_command("pytest")


def serve():
    """Run development server."""
    return run_command("python -m my_fastapi_project.cli.main serve --reload")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "lint":
            sys.exit(lint())
        elif command == "format":
            sys.exit(format_code())
        elif command == "test":
            sys.exit(test())
        elif command == "serve":
            sys.exit(serve())
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    else:
        print("Available commands: lint, format, test, serve")
```

### 7.2 Create .env File

Create `.env` for environment variables:

```env
# Application settings
PROJECT_NAME="My FastAPI Project"
ENVIRONMENT="development"
DEBUG=true

# Server settings
HOST="127.0.0.1"
PORT=8000

# Add your API keys and secrets here
# API_KEY=your-api-key-here
```

### 7.3 Update .gitignore

Add to `.gitignore`:

```gitignore
# Environment files
.env
.env.local
.env.*.local

# UV virtual environment
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Build artifacts
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# MyPy
.mypy_cache/
```

## 8. Development Workflow

### 8.1 Common Commands

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Format code
ruff format src/ tests/

# Lint code
ruff check src/ tests/

# Run tests
pytest

# Run tests with coverage
pytest --cov=my_fastapi_project --cov-report=html

# Start development server
python -m my_fastapi_project.cli.main serve --reload

# Or using the CLI directly
my-app serve --reload

# Type checking
mypy src/
```

### 8.2 Pre-commit Setup (Optional)

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

Install pre-commit:

```bash
uv pip install pre-commit
pre-commit install
```

## 9. Adding Document Processing (PyZerox Integration)

To add document processing capabilities like in InvoicePipe:

### 9.1 Add Dependencies

Update `pyproject.toml`:

```toml
dependencies = [
    # ... existing dependencies
    "quantalogic-pyzerox>=0.1.0",
    "python-magic>=0.4.27",
    "Pillow>=10.0.0",
    "PyPDF2>=3.0.0",
]
```

### 9.2 Create Document Processing Route

Create `src/my_fastapi_project/api/routes/documents.py`:

```python
"""Document processing endpoints."""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from my_fastapi_project.core.document_processor import process_document

router = APIRouter()


@router.post("/process-document")
async def process_document_endpoint(file: UploadFile = File(...)):
    """Process uploaded document."""
    try:
        # Validate file type
        if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Only PDF, PNG, and JPEG are supported."
            )
        
        # Process document
        result = await process_document(file)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 10. Deployment

### 10.1 Docker Support

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install dependencies
RUN uv pip install --system .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "my_fastapi_project.cli.main", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    volumes:
      - ./.env:/app/.env
```

### 10.2 Production Deployment

```bash
# Build production image
docker build -t my-fastapi-project .

# Run with Docker Compose
docker-compose up -d

# Or run directly
docker run -p 8000:8000 my-fastapi-project
```

## 11. Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [QuantaLogic PyZerox](https://github.com/quantalogic/quantalogic-pyzerox)

## 12. Related Documentation

- [InvoicePipe Project Overview](../README.md) - Main project documentation
- [InvoicePipe Specification](spec-invoice.md) - Detailed technical specification
- [Using QuantaLogic PyZerox](using-quantalogic-pyzerox.md) - Document processing guide
- [Managing Environment Variables and Configuration](managing-env-files.md) - Environment setup guide
- [Instructor Library Integration Guide](instructor-integration-guide.md) - Advanced structured data extraction patterns
- [LiteLLM Integration Guide](litellm-integration-guide.md) - Universal LLM gateway and cost management

## Learning Path

- [Step-by-Step Assignment: Building a Simple Invoice CLI Tool](preparation-work/step-by-step-assignment.md) - Build a simple CLI before tackling the full FastAPI project

## 13. Conclusion

This setup provides a solid foundation for a modern FastAPI project with:

- **Fast dependency management** with UV
- **Code quality tools** with Ruff
- **Type safety** with Pydantic and MyPy
- **Testing infrastructure** with Pytest
- **CLI interface** with Click
- **Modern packaging** with Hatchling
- **Production-ready** Docker deployment

The project structure is scalable and follows Python best practices, making it easy to extend and maintain as your application grows.
