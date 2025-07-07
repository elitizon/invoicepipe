Contributing
============

We welcome contributions to {{cookiecutter.project_name}}! This document provides guidelines for contributing to the project.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

   git clone https://github.com/{{cookiecutter.author_name}}/{{cookiecutter.project_slug}}.git
   cd {{cookiecutter.project_slug}}

3. Set up the development environment:

.. code-block:: bash

   # Create virtual environment with uv
   make venv
   
   # Install dependencies
   make install
   
   # Set up pre-commit hooks
   make pre-commit

4. Create a feature branch:

.. code-block:: bash

   git checkout -b feature/your-feature-name

Development Workflow
~~~~~~~~~~~~~~~~~~~

1. **Make your changes**: Implement your feature or fix
2. **Run tests**: Ensure all tests pass
3. **Check code quality**: Run linting and formatting
4. **Update documentation**: Add or update relevant documentation
5. **Commit your changes**: Use descriptive commit messages
6. **Push and create PR**: Submit your changes for review

Code Quality
------------

We maintain high code quality standards:

Testing
~~~~~~~

- **Write tests** for all new functionality
- **Maintain coverage** above 95%
- **Test edge cases** and error conditions
- **Use descriptive test names** that explain what is being tested

.. code-block:: bash

   # Run all tests
   make test
   
   # Run tests with coverage
   make test-cov
   
   # Run tests in watch mode
   make test-watch

Code Style
~~~~~~~~~~

We use automated code formatting and linting:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Bandit** for security analysis

.. code-block:: bash

   # Check code quality
   make check
   
   # Fix formatting issues
   make format
   
   # Fix linting issues
   make lint-fix

Documentation
~~~~~~~~~~~~~

- **Document public APIs** with clear docstrings
- **Update documentation** when changing functionality
- **Include examples** in docstrings
- **Write clear commit messages**

.. code-block:: bash

   # Build documentation
   make docs
   
   # Serve documentation locally
   make docs-serve

Pull Request Guidelines
-----------------------

Before submitting a pull request:

1. **Create an issue** describing the problem or enhancement
2. **Follow the development workflow** outlined above
3. **Ensure all tests pass**:

   .. code-block:: bash

      make ci

4. **Update documentation** if needed
5. **Write a clear PR description** explaining:
   - What changes were made
   - Why the changes were necessary
   - How to test the changes

Code Review Process
~~~~~~~~~~~~~~~~~~~

All pull requests undergo code review:

- **One approval required** from a project maintainer
- **All CI checks must pass** before merging
- **Address feedback** promptly and professionally
- **Keep PRs focused** - one feature/fix per PR

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Use clear, descriptive commit messages:

.. code-block:: text

   feat: add weather caching functionality
   
   - Implement in-memory cache for weather data
   - Add cache expiration logic
   - Update tests for cache behavior
   
   Fixes #123

Types of contributions:
- ``feat:`` new features
- ``fix:`` bug fixes
- ``docs:`` documentation changes
- ``test:`` test additions/changes
- ``refactor:`` code refactoring
- ``style:`` formatting changes

Bug Reports
-----------

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment information**:
   - Python version
   - Operating system
   - Package versions

Feature Requests
----------------

For feature requests, please:

1. **Check existing issues** to avoid duplicates
2. **Clearly describe** the desired functionality
3. **Explain the use case** and benefits
4. **Consider implementation** complexity

Community Guidelines
--------------------

We are committed to providing a welcoming and inclusive environment:

- **Be respectful** and professional
- **Welcome newcomers** and help them learn
- **Focus on constructive feedback**
- **Assume good intentions**

Code of Conduct
~~~~~~~~~~~~~~~

This project follows the `Contributor Covenant Code of Conduct <https://www.contributor-covenant.org/>`_.

Getting Help
------------

If you need help:

- **Check the documentation** first
- **Search existing issues** on GitHub
- **Ask questions** in GitHub Discussions
- **Join our community** chat (if available)

Release Process
---------------

For maintainers, the release process:

1. **Update version** in ``pyproject.toml``
2. **Update CHANGELOG** with new features and fixes
3. **Create release PR** with version bump
4. **Tag release** after PR merge
5. **Publish to PyPI** (automated via CI)

Development Tips
----------------

Useful commands for development:

.. code-block:: bash

   # Quick development cycle
   make check          # Fast quality check
   make run            # Test your changes
   
   # Full quality assurance
   make ci             # Complete CI pipeline
   
   # Debugging
   make debug          # Run with debug output
   make shell          # Interactive Python shell

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

For development, copy ``.env.example`` to ``.env`` and configure:

.. code-block:: bash

   cp .env.example .env
   # Edit .env with your settings

Common Issues
~~~~~~~~~~~~~

**Tests failing after checkout:**

.. code-block:: bash

   make clean
   make install
   make test

**Import errors:**

.. code-block:: bash

   # Ensure package is installed in development mode
   uv pip install -e .

**Pre-commit hooks failing:**

.. code-block:: bash

   make pre-commit

Thank you for contributing to {{cookiecutter.project_name}}!
