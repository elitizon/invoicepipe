"""{{cookiecutter.project_name}} package.

This package provides a simple Hello World FastAPI application with CLI support.
The application demonstrates basic web API functionality with clean architecture
and modern Python development practices.

Key Components:
    - main: The FastAPI application with endpoints
    - cli: Command line interface using Click
    - config: Configuration management
    - tools: Utility functions
    - exceptions: Custom exception hierarchy

Usage:
    >>> from {{cookiecutter.package_name}}.main import app
    >>> # Use app with uvicorn or other ASGI server

Version: {{cookiecutter.version}}
Author: {{cookiecutter.author_name}}
"""

from .config import settings
from .main import app

__version__ = "{{cookiecutter.version}}"
__author__ = "{{cookiecutter.author_name}}"
__email__ = "{{cookiecutter.author_email}}"

__all__ = ["app", "settings"]
