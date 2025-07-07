#!/usr/bin/env python3
"""
{{cookiecutter.project_name}} Runner

This script provides a simple way to run the FastAPI application.
It serves as an entry point for development and testing purposes.
"""

import uvicorn
from {{cookiecutter.package_name}}.config import settings


def main() -> None:
    """Run the FastAPI application with uvicorn."""
    print(f"Starting {settings.app_name}...")
    print(f"Version: {settings.version}")
    print(f"Server will be available at http://{settings.host}:{settings.port}")
    
    uvicorn.run(
        "{{cookiecutter.package_name}}.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
