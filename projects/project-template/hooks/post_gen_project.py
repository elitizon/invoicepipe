#!/usr/bin/env python3
"""Post-generation hook for ADK project template."""

import subprocess


def make_files_executable():
    """Make shell scripts executable."""
    # No shell scripts in this template, but keeping for future use
    pass


def initialize_git_repository():
    """Initialize git repository (optional)."""
    try:
        # Check if git is available
        subprocess.run(["git", "--version"], capture_output=True, check=True)

        # Initialize git repository
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")

        # Create initial commit would be done by user

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Git not found or failed to initialize repository")
        print("   You can initialize git manually later with: git init")


def show_next_steps():
    """Display next steps for the user."""
    project_name = "{{ cookiecutter.project_name }}"
    project_slug = "{{ cookiecutter.project_slug }}"

    print("\n" + "=" * 60)
    print(f"🎉 {project_name} created successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print(f"   cd {project_slug}")
    print("   make dev-setup     # Set up development environment")
    print("   make run           # Start your weather agent")
    print("\n🔧 Configure your environment:")
    print("   cp .env.example .env")
    print("   # Edit .env with your PROJECT_ID and LOCATION")
    print("\n📚 Learn more:")
    print("   make help          # See all available commands")
    print("   cat README.md      # Read the documentation")
    print("\n🚀 Happy building with Google ADK!")


if __name__ == "__main__":
    make_files_executable()
    initialize_git_repository()
    show_next_steps()
