"""Command line interface for {{cookiecutter.project_name}}.

This module provides the CLI commands for the Hello World application.
It includes commands for starting the server, running greetings, and getting app info.

Example:
    $ {{cookiecutter.project_slug}} serve
    $ {{cookiecutter.project_slug}} greet Alice
    $ {{cookiecutter.project_slug}} info
"""

import click
import uvicorn

from .config import settings
from .tools import create_greeting, get_app_info


@click.group()
@click.version_option(version=settings.version)
def main() -> None:
    """{{cookiecutter.project_name}} CLI."""
    pass


@main.command()
@click.option(
    "--host",
    default=settings.host,
    help="Host to bind the server to",
    show_default=True,
)
@click.option(
    "--port",
    default=settings.port,
    help="Port to bind the server to",
    show_default=True,
)
@click.option(
    "--reload",
    is_flag=True,
    help="Enable auto-reload for development",
)
def serve(host: str, port: int, reload: bool) -> None:
    """Start the FastAPI server."""
    click.echo(f"Starting {settings.app_name} server...")
    click.echo(f"Server will be available at http://{host}:{port}")
    
    uvicorn.run(
        "{{cookiecutter.package_name}}.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@main.command()
@click.argument("name", required=False)
@click.option(
    "--greeting",
    default="Hello",
    help="Type of greeting to use",
    show_default=True,
)
def greet(name: str | None, greeting: str) -> None:
    """Create a greeting message."""
    if name is None:
        name = "World"
    
    message = create_greeting(name, greeting)
    click.echo(message)


@main.command()
def info() -> None:
    """Show application information."""
    app_info = get_app_info()
    
    click.echo(f"Application: {settings.app_name}")
    click.echo(f"Version: {settings.version}")
    click.echo(f"Description: {settings.description}")
    click.echo(f"Message: {app_info['message']}")
    click.echo(f"Available endpoints: {app_info['endpoints']}")


if __name__ == "__main__":
    main()
