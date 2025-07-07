# Managing Environment Variables and Configuration with .env Files

This guide explains how to effectively manage environment variables and configuration in Python applications using `.env` files and the `python-dotenv` library, as used in the InvoicePipe project.

## Why Use Environment Variables?

Environment variables provide a secure and flexible way to manage configuration settings, API keys, database URLs, and other sensitive information without hardcoding them into your source code.

### Benefits:
- **Security**: Keep sensitive data out of version control
- **Flexibility**: Different configurations for development, staging, and production
- **Portability**: Easy deployment across different environments
- **Best Practices**: Follows the [12-Factor App](https://12factor.net/config) methodology

## 1. Installing python-dotenv

```bash
# Using UV (recommended)
uv pip install python-dotenv

# Using pip
pip install python-dotenv
```

Add to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "python-dotenv>=1.0.0",
    # ... other dependencies
]
```

## 2. Creating .env Files

### 2.1 Basic .env File Structure

Create a `.env` file in your project root:

```env
# Application Settings
PROJECT_NAME="InvoicePipe"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# Server Configuration
HOST="127.0.0.1"
PORT=8000

# API Keys (Keep these secret!)
OPENAI_API_KEY="sk-your-openai-key-here"
GEMINI_API_KEY="your-gemini-key-here"
ANTHROPIC_API_KEY="your-anthropic-key-here"

# Database URLs
DATABASE_URL="postgresql://user:password@localhost/dbname"
REDIS_URL="redis://localhost:6379"

# Security Settings
SECRET_KEY="your-super-secret-key-here"
ALLOWED_HOSTS="localhost,127.0.0.1"

# File Processing Settings
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR="./uploads"
TEMP_DIR="./temp"

# Logging
LOG_LEVEL="INFO"
LOG_FORMAT="json"
```

### 2.2 Environment-Specific Files

Create different `.env` files for different environments:

```bash
.env                 # Default/development
.env.local           # Local overrides (not in git)
.env.production      # Production settings
.env.staging         # Staging settings
.env.test            # Test environment
```

## 3. Using python-dotenv in Your Application

### 3.1 Basic Usage

```python
"""Loading environment variables with python-dotenv."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
port = int(os.getenv("PORT", "8000"))

print(f"API Key: {api_key}")
print(f"Debug Mode: {debug_mode}")
print(f"Port: {port}")
```

### 3.2 Advanced Loading Options

```python
"""Advanced dotenv loading options."""

from dotenv import load_dotenv, find_dotenv
import os

# Load from specific file
load_dotenv(".env.production")

# Load from automatically found .env file
load_dotenv(find_dotenv())

# Load with override option
load_dotenv(override=True)  # Override existing env vars

# Load from different directory
load_dotenv(dotenv_path="config/.env")

# Load with verbose output
load_dotenv(verbose=True)
```

### 3.3 Using with Pydantic Settings

This is the recommended approach for FastAPI applications:

```python
"""Configuration management with Pydantic BaseSettings."""

from pydantic import BaseSettings, Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings with automatic .env loading."""
    
    # Application
    project_name: str = Field(default="InvoicePipe", env="PROJECT_NAME")
    version: str = Field(default="1.0.0", env="VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Server
    host: str = Field(default="127.0.0.1", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # API Keys
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Database
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Security
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")
    allowed_hosts: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    
    # File Processing
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    temp_dir: str = Field(default="./temp", env="TEMP_DIR")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        # Support multiple env files (order matters)
        env_file = [".env", ".env.local"]

# Create global settings instance
settings = Settings()

# Usage example
print(f"Project: {settings.project_name}")
print(f"Environment: {settings.environment}")
print(f"Debug Mode: {settings.debug}")
```

## 4. Best Practices

### 4.1 .env File Organization

```env
# ===========================================
# APPLICATION CONFIGURATION
# ===========================================
PROJECT_NAME="InvoicePipe"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# ===========================================
# SERVER SETTINGS
# ===========================================
HOST="127.0.0.1"
PORT=8000
WORKERS=4

# ===========================================
# API KEYS & SECRETS
# ===========================================
# OpenAI Configuration
OPENAI_API_KEY="sk-your-key-here"
OPENAI_MODEL="gpt-4o"

# Gemini Configuration  
GEMINI_API_KEY="your-gemini-key"
GEMINI_MODEL="gemini-2.0-flash-exp"

# Anthropic Configuration
ANTHROPIC_API_KEY="your-anthropic-key"
ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"

# ===========================================
# DATABASE & STORAGE
# ===========================================
DATABASE_URL="postgresql://user:pass@localhost/invoicepipe"
REDIS_URL="redis://localhost:6379/0"

# ===========================================
# SECURITY
# ===========================================
SECRET_KEY="your-super-secret-key-minimum-32-characters"
ALLOWED_HOSTS="localhost,127.0.0.1,your-domain.com"
CORS_ORIGINS="http://localhost:3000,https://your-frontend.com"

# ===========================================
# FILE PROCESSING
# ===========================================
MAX_FILE_SIZE=10485760          # 10MB in bytes
SUPPORTED_FORMATS="pdf,png,jpg,jpeg"
UPLOAD_DIR="./uploads"
TEMP_DIR="./temp"
CLEANUP_TEMP_FILES=true

# ===========================================
# LOGGING & MONITORING
# ===========================================
LOG_LEVEL="INFO"
LOG_FORMAT="json"
ENABLE_METRICS=true
METRICS_PORT=9090
```

### 4.2 Environment-Specific Configurations

**Development (.env.development):**
```env
ENVIRONMENT="development"
DEBUG=true
LOG_LEVEL="DEBUG"
DATABASE_URL="postgresql://dev:dev@localhost/invoicepipe_dev"
```

**Production (.env.production):**
```env
ENVIRONMENT="production"
DEBUG=false
LOG_LEVEL="INFO"
DATABASE_URL="postgresql://prod_user:secure_pass@prod-db/invoicepipe"
SECRET_KEY="production-secret-key-very-long-and-secure"
```

**Testing (.env.test):**
```env
ENVIRONMENT="test"
DEBUG=false
LOG_LEVEL="WARNING"
DATABASE_URL="postgresql://test:test@localhost/invoicepipe_test"
```

### 4.3 Validation and Type Conversion

```python
"""Environment variable validation and type conversion."""

from pydantic import BaseSettings, validator, Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Settings with validation and type conversion."""
    
    # String with validation
    environment: str = Field(env="ENVIRONMENT")
    
    @validator("environment")
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production", "test"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    # List from comma-separated string
    allowed_hosts: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    
    @validator("allowed_hosts", pre=True)
    def parse_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    # File size with human-readable format
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")
    
    @validator("max_file_size", pre=True)
    def parse_file_size(cls, v):
        if isinstance(v, str):
            # Support formats like "10MB", "1GB", etc.
            v = v.upper()
            if v.endswith("MB"):
                return int(float(v[:-2]) * 1024 * 1024)
            elif v.endswith("GB"):
                return int(float(v[:-2]) * 1024 * 1024 * 1024)
            elif v.endswith("KB"):
                return int(float(v[:-2]) * 1024)
        return int(v)
    
    # Optional URL with validation
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    
    @validator("database_url")
    def validate_database_url(cls, v):
        if v and not v.startswith(("postgresql://", "mysql://", "sqlite://")):
            raise ValueError("Database URL must start with postgresql://, mysql://, or sqlite://")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True
```

## 5. Security Best Practices

### 5.1 .gitignore Configuration

Always add environment files to `.gitignore`:

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.production
.env.staging

# But allow example files
!.env.example
!.env.template
```

### 5.2 Create .env.example

Provide a template for other developers:

```env
# Copy this file to .env and fill in your values

# ===========================================
# APPLICATION CONFIGURATION
# ===========================================
PROJECT_NAME="InvoicePipe"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# ===========================================
# API KEYS (Required)
# ===========================================
OPENAI_API_KEY="your-openai-api-key-here"
GEMINI_API_KEY="your-gemini-api-key-here"
ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# ===========================================
# DATABASE (Optional for development)
# ===========================================
DATABASE_URL="postgresql://user:password@localhost/invoicepipe"

# ===========================================
# SECURITY (Generate secure keys for production)
# ===========================================
SECRET_KEY="your-secret-key-here"
```

### 5.3 Secret Generation

```python
"""Generate secure secrets for production."""

import secrets
import string

def generate_secret_key(length: int = 50) -> str:
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_api_key(length: int = 32) -> str:
    """Generate a secure API key."""
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print(f"SECRET_KEY={generate_secret_key()}")
    print(f"API_KEY={generate_api_key()}")
```

## 6. Advanced Usage Patterns

### 6.1 Hierarchical Configuration

```python
"""Hierarchical configuration with multiple sources."""

from pydantic import BaseSettings
from typing import Optional

class DatabaseSettings(BaseSettings):
    """Database-specific settings."""
    url: Optional[str] = None
    pool_size: int = 10
    echo: bool = False
    
    class Config:
        env_prefix = "DB_"
        env_file = ".env"

class RedisSettings(BaseSettings):
    """Redis-specific settings."""
    url: str = "redis://localhost:6379"
    password: Optional[str] = None
    db: int = 0
    
    class Config:
        env_prefix = "REDIS_"
        env_file = ".env"

class Settings(BaseSettings):
    """Main application settings."""
    project_name: str = "InvoicePipe"
    version: str = "1.0.0"
    
    # Nested settings
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    
    class Config:
        env_file = ".env"
```

Example `.env` file:
```env
PROJECT_NAME="InvoicePipe"
VERSION="1.0.0"

# Database settings (with DB_ prefix)
DB_URL="postgresql://user:pass@localhost/invoicepipe"
DB_POOL_SIZE=20
DB_ECHO=true

# Redis settings (with REDIS_ prefix)
REDIS_URL="redis://localhost:6379"
REDIS_PASSWORD="secret"
REDIS_DB=1
```

### 6.2 Dynamic Environment Loading

```python
"""Dynamic environment loading based on conditions."""

from dotenv import load_dotenv
import os
from pathlib import Path

def load_environment():
    """Load environment variables based on current environment."""
    
    # Determine environment
    env = os.getenv("ENVIRONMENT", "development")
    
    # Load base .env file
    base_env = Path(".env")
    if base_env.exists():
        load_dotenv(base_env)
    
    # Load environment-specific file
    env_file = Path(f".env.{env}")
    if env_file.exists():
        load_dotenv(env_file, override=True)
    
    # Load local overrides
    local_env = Path(".env.local")
    if local_env.exists():
        load_dotenv(local_env, override=True)
    
    print(f"Loaded environment: {env}")

# Usage
load_environment()
```

### 6.3 Configuration Validation

```python
"""Configuration validation and health checks."""

from pydantic import BaseSettings, ValidationError
import sys
import os

class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Required settings
    openai_api_key: str = Field(..., min_length=10, env="OPENAI_API_KEY")
    secret_key: str = Field(..., min_length=32, env="SECRET_KEY")
    
    # Optional with defaults
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    class Config:
        env_file = ".env"

def validate_configuration():
    """Validate configuration and exit if invalid."""
    try:
        settings = Settings()
        print("✅ Configuration validation successful")
        return settings
    except ValidationError as e:
        print("❌ Configuration validation failed:")
        for error in e.errors():
            field = error["loc"][0]
            message = error["msg"]
            print(f"  - {field}: {message}")
        sys.exit(1)

# Usage
if __name__ == "__main__":
    settings = validate_configuration()
```

## 7. Integration with FastAPI

### 7.1 FastAPI Configuration

```python
"""FastAPI application with environment configuration."""

from fastapi import FastAPI, Depends
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    project_name: str = "InvoicePipe"
    version: str = "1.0.0"
    debug: bool = True
    openai_api_key: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Get cached settings instance."""
    return Settings()

# FastAPI app
app = FastAPI(
    title="InvoicePipe API",
    version="1.0.0",
    debug=get_settings().debug,
)

@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    """Get current configuration (safe fields only)."""
    return {
        "project_name": settings.project_name,
        "version": settings.version,
        "debug": settings.debug,
        "environment": settings.environment,
        # Don't expose sensitive data like API keys
    }
```

### 7.2 Environment-Specific Startup

```python
"""Environment-specific FastAPI startup."""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with environment-specific setup."""
    settings = get_settings()
    
    # Environment-specific setup
    if settings.environment == "production":
        # Production setup
        logging.getLogger().setLevel(logging.INFO)
        # Initialize production resources
    elif settings.environment == "development":
        # Development setup
        logging.getLogger().setLevel(logging.DEBUG)
        # Initialize development resources
    
    yield
    
    # Cleanup
    # Close database connections, etc.

app = FastAPI(lifespan=lifespan)
```

## 8. Common Patterns and Examples

### 8.1 InvoicePipe Configuration

```python
"""InvoicePipe-specific configuration example."""

from pydantic import BaseSettings, Field, validator
from typing import List, Optional, Dict, Any
import os

class InvoicePipeSettings(BaseSettings):
    """InvoicePipe application settings."""
    
    # Application
    project_name: str = Field(default="InvoicePipe", env="PROJECT_NAME")
    version: str = Field(default="1.0.0", env="VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Server
    host: str = Field(default="127.0.0.1", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # API Keys for document processing
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash-exp", env="GEMINI_MODEL")
    
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    
    # File processing
    max_file_size: str = Field(default="10MB", env="MAX_FILE_SIZE")
    supported_formats: List[str] = Field(default=["pdf", "png", "jpg", "jpeg"], env="SUPPORTED_FORMATS")
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    temp_dir: str = Field(default="./temp", env="TEMP_DIR")
    cleanup_temp_files: bool = Field(default=True, env="CLEANUP_TEMP_FILES")
    
    # Processing options
    default_concurrency: int = Field(default=5, env="DEFAULT_CONCURRENCY")
    processing_timeout: int = Field(default=300, env="PROCESSING_TIMEOUT")  # 5 minutes
    
    @validator("max_file_size", pre=True)
    def parse_file_size(cls, v):
        """Convert human-readable file size to bytes."""
        if isinstance(v, str):
            v = v.upper()
            if v.endswith("MB"):
                return int(float(v[:-2]) * 1024 * 1024)
            elif v.endswith("GB"):
                return int(float(v[:-2]) * 1024 * 1024 * 1024)
            elif v.endswith("KB"):
                return int(float(v[:-2]) * 1024)
        return int(v)
    
    @validator("supported_formats", pre=True)
    def parse_formats(cls, v):
        """Parse comma-separated formats."""
        if isinstance(v, str):
            return [fmt.strip().lower() for fmt in v.split(",")]
        return v
    
    @property
    def api_v1_str(self) -> str:
        """API v1 prefix."""
        return "/api/v1"
    
    @property
    def has_ai_provider(self) -> bool:
        """Check if at least one AI provider is configured."""
        return bool(self.openai_api_key or self.gemini_api_key or self.anthropic_api_key)
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI provider configuration."""
        config = {}
        
        if self.openai_api_key:
            config["openai"] = {
                "api_key": self.openai_api_key,
                "model": self.openai_model
            }
        
        if self.gemini_api_key:
            config["gemini"] = {
                "api_key": self.gemini_api_key,
                "model": self.gemini_model
            }
        
        if self.anthropic_api_key:
            config["anthropic"] = {
                "api_key": self.anthropic_api_key,
                "model": self.anthropic_model
            }
        
        return config
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Custom environment variable parsing."""
            if field_name == "DEBUG":
                return raw_val.lower() in ("true", "1", "yes", "on")
            return cls.json_loads(raw_val)

# Global settings instance
settings = InvoicePipeSettings()
```

### 8.2 Corresponding .env File

```env
# InvoicePipe Configuration

# ===========================================
# APPLICATION SETTINGS
# ===========================================
PROJECT_NAME="InvoicePipe"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# ===========================================
# SERVER CONFIGURATION
# ===========================================
HOST="127.0.0.1"
PORT=8000
WORKERS=4

# ===========================================
# AI PROVIDER CONFIGURATION
# ===========================================
# OpenAI (Primary)
OPENAI_API_KEY="sk-your-openai-api-key-here"
OPENAI_MODEL="gpt-4o"

# Google Gemini (Alternative)
GEMINI_API_KEY="your-gemini-api-key-here"
GEMINI_MODEL="gemini-2.0-flash-exp"

# Anthropic Claude (Alternative)
ANTHROPIC_API_KEY="your-anthropic-api-key-here"
ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"

# ===========================================
# FILE PROCESSING SETTINGS
# ===========================================
MAX_FILE_SIZE="10MB"
SUPPORTED_FORMATS="pdf,png,jpg,jpeg"
UPLOAD_DIR="./uploads"
TEMP_DIR="./temp"
CLEANUP_TEMP_FILES=true

# ===========================================
# PROCESSING OPTIONS
# ===========================================
DEFAULT_CONCURRENCY=5
PROCESSING_TIMEOUT=300

# ===========================================
# SECURITY & MONITORING
# ===========================================
SECRET_KEY="your-secret-key-here-min-32-chars"
ALLOWED_HOSTS="localhost,127.0.0.1"
LOG_LEVEL="INFO"
```

## 9. Testing with Environment Variables

### 9.1 Test Configuration

```python
"""Test configuration with environment variables."""

import pytest
import os
from unittest.mock import patch
from your_app.config import Settings

@pytest.fixture
def test_env_vars():
    """Test environment variables."""
    return {
        "PROJECT_NAME": "TestApp",
        "DEBUG": "false",
        "OPENAI_API_KEY": "test-key",
        "MAX_FILE_SIZE": "5MB",
    }

@pytest.fixture
def test_settings(test_env_vars):
    """Test settings with mocked environment."""
    with patch.dict(os.environ, test_env_vars):
        yield Settings()

def test_settings_loading(test_settings):
    """Test that settings load correctly."""
    assert test_settings.project_name == "TestApp"
    assert test_settings.debug is False
    assert test_settings.openai_api_key == "test-key"
    assert test_settings.max_file_size == 5 * 1024 * 1024  # 5MB in bytes

def test_settings_validation():
    """Test settings validation."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "short"}):
        with pytest.raises(ValueError):
            Settings()
```

### 9.2 Test .env File

Create `.env.test`:

```env
# Test environment configuration
PROJECT_NAME="InvoicePipe Test"
ENVIRONMENT="test"
DEBUG=false
OPENAI_API_KEY="test-key-for-testing"
MAX_FILE_SIZE="1MB"
TEMP_DIR="./test_temp"
```

## 10. Deployment and Production

### 10.1 Production Environment Setup

```bash
# Production environment variables
export PROJECT_NAME="InvoicePipe"
export ENVIRONMENT="production"
export DEBUG="false"
export OPENAI_API_KEY="your-production-openai-key"
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="postgresql://user:pass@prod-db/invoicepipe"
export REDIS_URL="redis://prod-redis:6379"
export LOG_LEVEL="INFO"
```

### 10.2 Docker Integration

```dockerfile
# Dockerfile with environment support
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install uv && uv pip install --system .

# Copy application
COPY src/ ./src/

# Set default environment variables
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "invoicepipe.cli.main", "serve"]
```

Docker Compose with environment file:

```yaml
version: '3.8'

services:
  invoicepipe:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
```

## 11. Related Documentation

- [InvoicePipe Project Overview](../README.md)
- [InvoicePipe Specification](spec-invoice.md)
- [Setting Up a FastAPI Project](setup-fastapi-project.md)
- [Using QuantaLogic PyZerox](using-quantalogic-pyzerox.md)

## Learning Path

- [Step-by-Step Assignment: Building a Simple Invoice CLI Tool](preparation-work/step-by-step-assignment.md) - Practice environment variable management with a simple CLI project

## 12. Additional Resources

- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [12-Factor App Configuration](https://12factor.net/config)
- [FastAPI Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)

## Conclusion

Proper environment variable management is crucial for building secure, maintainable, and deployable applications. By using `.env` files with `python-dotenv` and Pydantic Settings, you can create a robust configuration system that works across different environments while keeping sensitive information secure.

Remember to:
- Never commit `.env` files to version control
- Use `.env.example` files as templates
- Validate your configuration at startup
- Use environment-specific configurations
- Keep sensitive data in environment variables, not in code
