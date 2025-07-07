#!/usr/bin/env python3
"""Pre-generation hook for ADK project template validation."""

import re
import sys


def validate_project_name():
    """Ensure project name follows conventions."""
    project_name = "{{ cookiecutter.project_name }}"

    # Check if project name is not empty
    if not project_name.strip():
        print("ERROR: Project name cannot be empty")
        sys.exit(1)

    # Check if project name contains only allowed characters
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9\s\-_]*$", project_name):
        print(f"ERROR: Invalid project name '{project_name}'")
        print(
            "Project name must start with a letter and contain only letters, numbers, spaces, hyphens, and underscores"
        )
        sys.exit(1)

    # Check length
    if len(project_name) < 3:
        print("ERROR: Project name must be at least 3 characters long")
        sys.exit(1)

    if len(project_name) > 50:
        print("ERROR: Project name must be no more than 50 characters long")
        sys.exit(1)


def validate_email():
    """Basic email validation."""
    email = "{{ cookiecutter.author_email }}"

    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        print(f"ERROR: Invalid email format '{email}'")
        sys.exit(1)


if __name__ == "__main__":
    validate_project_name()
    validate_email()
    print("✅ Template validation passed")
