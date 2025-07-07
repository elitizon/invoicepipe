# 🚀 {{cookiecutter.project_name}} - Developer Makefile
# Modern Python development workflow with uv and quality gates

# Colors for better terminal output
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m
BOLD := \033[1m

# Project configuration
PROJECT_NAME := {{cookiecutter.project_slug}}
PYTHON_VERSION := {{cookiecutter.python_version}}
SRC_DIR := {{cookiecutter.package_name}}
TEST_DIR := tests

.PHONY: help install lint test format clean run venv dev-setup pre-commit all

# Default target
all: help

help: ## 📖 Show this help message
	@echo "$(BOLD)$(CYAN)🚀 $(PROJECT_NAME) Development Commands$(RESET)"
	@echo ""
	@echo "$(BOLD)🏗️  Setup & Installation:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"; print ""} /^[a-zA-Z_-]+:.*?##/ { if ($$2 ~ /🏗️|📦|🔧/) printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)✅ Code Quality & Testing:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"; print ""} /^[a-zA-Z_-]+:.*?##/ { if ($$2 ~ /✅|🧪|🔍|🛡️|🎯/) printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)🏃 Running & Development:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"; print ""} /^[a-zA-Z_-]+:.*?##/ { if ($$2 ~ /🏃|🌐|📚|🧹/) printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)💡 Quick Start:$(RESET)"
	@echo "  $(CYAN)make dev-setup$(RESET)   # Complete development environment setup"
	@echo "  $(GREEN)make check$(RESET)       # Run all quality checks quickly"
	@echo "  $(YELLOW)make run$(RESET)         # Start the agent"
	@echo ""

# =============================================================================
# 🏗️ Environment Setup
# =============================================================================

venv: ## 🔧 Create Python virtual environment with uv
	@if [ ! -d .venv ]; then \
		echo "$(CYAN)Creating virtual environment...$(RESET)"; \
		uv venv .venv; \
		echo "$(GREEN)✅ Virtual environment created at .venv$(RESET)"; \
		echo "$(YELLOW)💡 Activate with: source .venv/bin/activate$(RESET)"; \
	else \
		echo "$(GREEN)✅ Virtual environment already exists$(RESET)"; \
	fi

.venv: ## 📦 Ensure virtual environment exists
	@$(MAKE) venv

install: .venv ## 📦 Install all dependencies (production + development + docs)
	@echo "$(CYAN)Installing dependencies (dev + docs)...$(RESET)"
	@if [ ! -f .venv/bin/ruff ]; then \
		uv sync --extra dev --extra docs; \
	else \
		echo "$(GREEN)✅ Dependencies already installed$(RESET)"; \
	fi
	@echo "$(GREEN)✅ All dependencies ready$(RESET)"

dev-setup: venv install pre-commit ## 🏗️ Complete development environment setup
	@echo "$(GREEN)🎉 Development environment setup complete!$(RESET)"
	@echo "$(YELLOW)💡 Run 'make check' to validate your setup$(RESET)"

# =============================================================================
# ✅ Code Quality & Testing
# =============================================================================

check: lint typecheck test ## 🎯 Quick quality check (lint + type + test)
	@echo "$(GREEN)🎉 All quick checks passed!$(RESET)"

test: .venv ## 🧪 Run all tests with pytest
	@echo "$(CYAN)Running tests...$(RESET)"
	@uv run pytest --tb=short --maxfail=3 tests
	@echo "$(GREEN)✅ All tests passed$(RESET)"

test-cov: .venv ## 🧪 Run tests with coverage reporting
	@echo "$(CYAN)Running tests with coverage...$(RESET)"
	@uv run pytest --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html --tb=short --maxfail=3 tests
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/$(RESET)"

test-watch: .venv ## 🧪 Run tests in watch mode (re-run on file changes)
	@echo "$(CYAN)Starting test watch mode...$(RESET)"
	@echo "$(YELLOW)💡 Press Ctrl+C to stop$(RESET)"
	@uv run pytest-watch --clear --onpass="echo '$(GREEN)✅ Tests passed$(RESET)'" --onfail="echo '$(RED)❌ Tests failed$(RESET)'"

lint: .venv ## 🔍 Run ruff linting (check only)
	@echo "$(CYAN)Linting code...$(RESET)"
	@uv run ruff check $(SRC_DIR) tests
	@echo "$(GREEN)✅ Linting passed$(RESET)"

lint-fix: .venv ## 🔍 Run ruff linting with auto-fix
	@echo "$(CYAN)Fixing linting issues...$(RESET)"
	@uv run ruff check --fix $(SRC_DIR) tests
	@echo "$(GREEN)✅ Linting issues fixed$(RESET)"

format: .venv ## 🔍 Format code with ruff
	@echo "$(CYAN)Formatting code...$(RESET)"
	@uv run ruff format $(SRC_DIR) tests
	@echo "$(GREEN)✅ Code formatted$(RESET)"

format-check: .venv ## 🔍 Check code formatting (no changes)
	@echo "$(CYAN)Checking code formatting...$(RESET)"
	@uv run ruff format --check $(SRC_DIR) tests
	@echo "$(GREEN)✅ Code formatting is correct$(RESET)"

typecheck: .venv ## 🔍 Run mypy type checking
	@echo "$(CYAN)Type checking...$(RESET)"
	@uv run mypy $(SRC_DIR) --python-version $(PYTHON_VERSION)
	@echo "$(GREEN)✅ Type checking passed$(RESET)"

security: .venv ## 🛡️ Run security checks with bandit
	@echo "$(CYAN)Running security checks...$(RESET)"
	@uv run bandit -r $(SRC_DIR) -ll || echo "$(YELLOW)⚠️ Some security warnings found$(RESET)"
	@echo "$(GREEN)✅ Security scan completed$(RESET)"

audit: .venv ## 🛡️ Check for known vulnerabilities in dependencies
	@echo "$(CYAN)Auditing dependencies...$(RESET)"
	@uv run pip-audit
	@echo "$(GREEN)✅ Dependency audit completed$(RESET)"

pre-commit: .venv ## ✅ Install and run pre-commit hooks
	@echo "$(CYAN)Setting up pre-commit hooks...$(RESET)"
	@uv run pre-commit install
	@echo "$(CYAN)Running pre-commit on all files...$(RESET)"
	@uv run pre-commit run --all-files
	@echo "$(GREEN)✅ Pre-commit hooks setup and validated$(RESET)"

quality: lint format-check typecheck security ## ✅ Run all quality checks
	@echo "$(GREEN)🏆 All quality checks passed!$(RESET)"

# =============================================================================
# 🏃 Running & Development
# =============================================================================

run: .venv ## 🏃 Run the {{cookiecutter.project_name}}
	@echo "$(CYAN)Starting {{cookiecutter.project_name}}...$(RESET)"
	@echo "$(YELLOW)💡 Press Ctrl+C to stop$(RESET)"
	@uv run python run_agent.py

adk-web: .venv ## 🌐 Launch ADK web interface
	@echo "$(CYAN)Starting ADK web interface...$(RESET)"
	@echo "$(YELLOW)💡 Open your browser to the displayed URL$(RESET)"
	@uv run adk web

debug: .venv ## 🏃 Run agent in debug mode with verbose output
	@echo "$(CYAN)Starting agent in debug mode...$(RESET)"
	@DEBUG=true uv run python run_agent.py

shell: .venv ## 🏃 Start interactive Python shell with project loaded
	@echo "$(CYAN)Starting interactive shell...$(RESET)"
	@echo "$(YELLOW)💡 Project modules are available for import$(RESET)"
	@uv run python -i -c "from {{cookiecutter.package_name}} import *; print('{{cookiecutter.project_name}} modules loaded')"

# =============================================================================
# 📚 Documentation & Utilities
# =============================================================================

docs: .venv ## 📚 Generate documentation with Sphinx
	@echo "$(CYAN)Generating documentation...$(RESET)"
	@uv run sphinx-build -b html docs docs/_build/html
	@echo "$(GREEN)✅ Documentation generated in docs/_build/html/$(RESET)"

docs-serve: docs ## 📚 Generate and serve documentation locally
	@echo "$(CYAN)Serving documentation at http://localhost:8000$(RESET)"
	@echo "$(YELLOW)💡 Press Ctrl+C to stop$(RESET)"
	@cd docs/_build/html && python -m http.server 8000

status: .venv ## 📚 Show project status and health check
	@echo "$(BOLD)$(CYAN)🔍 $(PROJECT_NAME) Status$(RESET)"
	@echo ""
	@echo "$(BOLD)Python Environment:$(RESET)"
	@uv run python --version
	@echo "Virtual env: $$(pwd)/.venv"
	@echo ""
	@echo "$(BOLD)Dependencies:$(RESET)"
	@uv run pip list | grep -E "(ruff|pytest|mypy|google-adk)" || echo "Core dependencies not found"
	@echo ""
	@echo "$(BOLD)Project Structure:$(RESET)"
	@ls -la $(SRC_DIR)/ | head -5
	@echo ""
	@echo "$(BOLD)Last Commit:$(RESET)"
	@git log --oneline -1 2>/dev/null || echo "Not a git repository"
	@echo ""
	@echo "$(BOLD)Quick Health Check:$(RESET)"
	@echo -n "Configuration: "
	@uv run python -c "from {{cookiecutter.package_name}}.config import Config; print('✅ OK' if Config.is_configured() else '⚠️  Needs setup')" 2>/dev/null || echo "❌ Error"

# =============================================================================
# 🧹 Cleanup & Maintenance
# =============================================================================

clean: ## 🧹 Remove build artifacts and cache files
	@echo "$(CYAN)Cleaning up...$(RESET)"
	@rm -rf __pycache__ $(SRC_DIR)/__pycache__ $(TEST_DIR)/__pycache__
	@find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov coverage.xml .coverage
	@rm -rf docs/_build
	@echo "$(GREEN)✅ Cleanup completed$(RESET)"

clean-all: clean ## 🧹 Remove everything including virtual environment
	@echo "$(YELLOW)⚠️  This will remove the virtual environment!$(RESET)"
	@read -p "Are you sure? (y/N) " -n 1 -r; echo; if [[ $$REPLY =~ ^[Yy]$$ ]]; then rm -rf .venv; echo "$(GREEN)✅ Virtual environment removed$(RESET)"; else echo "$(YELLOW)Cancelled$(RESET)"; fi

reset: clean-all dev-setup ## 🧹 Complete reset: clean everything and rebuild
	@echo "$(GREEN)🎉 Project reset completed!$(RESET)"

# =============================================================================
# 🚀 Advanced Development Commands
# =============================================================================

ci: ## 🎯 Run full CI pipeline locally
	@echo "$(BOLD)$(CYAN)🚀 Running full CI pipeline...$(RESET)"
	@echo ""
	@echo "$(CYAN)1/5 - Linting...$(RESET)"
	@$(MAKE) lint
	@echo ""
	@echo "$(CYAN)2/5 - Type checking...$(RESET)"
	@$(MAKE) typecheck
	@echo ""
	@echo "$(CYAN)3/5 - Testing...$(RESET)"
	@$(MAKE) test-cov
	@echo ""
	@echo "$(CYAN)4/5 - Security scan...$(RESET)"
	@$(MAKE) security
	@echo ""
	@echo "$(CYAN)5/5 - Dependency audit...$(RESET)"
	@$(MAKE) audit
	@echo ""
	@echo "$(BOLD)$(GREEN)🏆 Full CI pipeline completed successfully!$(RESET)"

benchmark: .venv ## 🎯 Run performance benchmarks
	@echo "$(CYAN)Running performance benchmarks...$(RESET)"
	@uv run python -m pytest tests/ -k "performance" -v --tb=short
	@echo "$(GREEN)✅ Benchmarks completed$(RESET)"

fix: .venv ## 🔧 Auto-fix all fixable issues (format + lint-fix)
	@echo "$(CYAN)Auto-fixing all issues...$(RESET)"
	@$(MAKE) format
	@$(MAKE) lint-fix
	@echo "$(GREEN)✅ Auto-fixes applied$(RESET)"

outdated: .venv ## 📦 Check for outdated dependencies
	@echo "$(CYAN)Checking for outdated dependencies...$(RESET)"
	@uv run pip list --outdated

update-deps: .venv ## 📦 Update all dependencies to latest versions
	@echo "$(YELLOW)⚠️  This will update all dependencies!$(RESET)"
	@read -p "Continue? (y/N) " -n 1 -r; echo; if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(CYAN)Updating dependencies...$(RESET)"; \
		uv pip install --upgrade pip --python .venv/bin/python; \
		uv pip install --upgrade -e . --python .venv/bin/python; \
		echo "$(GREEN)✅ Dependencies updated$(RESET)"; \
	else \
		echo "$(YELLOW)Cancelled$(RESET)"; \
	fi
