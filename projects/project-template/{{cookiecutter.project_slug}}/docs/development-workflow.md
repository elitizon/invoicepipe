# Development Workflow Guide

This guide covers the daily development workflow for working with {{cookiecutter.project_name}}.

## 🚀 Quick Start for Development

### Initial Setup

```bash
# Clone and setup
git clone https://github.com/{{cookiecutter.author_name}}/{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}

# Complete development environment setup
make dev-setup

# Verify installation
make status
```

### Daily Development Commands

```bash
# Quick quality check (runs frequently during development)
make check          # lint + typecheck + test (fast)

# Run your agent
make run            # Start the agent for testing

# Auto-fix common issues
make fix            # format + lint-fix

# Full quality assurance (before committing)
make ci             # Complete CI pipeline
```

## 🔄 Development Cycle

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Check your work frequently
make check          # Quick validation (30 seconds)

# Test your changes
make run            # Start agent to test interactively
```

### 2. Quality Assurance

```bash
# Before committing, run full checks
make ci             # Complete quality pipeline

# Or run individual checks
make test-cov       # Tests with coverage
make lint           # Code linting
make typecheck      # Type checking
make security       # Security analysis
```

### 3. Documentation

```bash
# Update documentation if needed
make docs           # Build documentation
make docs-serve     # View docs locally (http://localhost:8000)
```

### 4. Commit and Push

```bash
# Stage and commit changes
git add .
git commit -m "feat: add new weather feature"

# Push changes
git push origin feature/your-feature-name
```

## 📋 Available Commands

### Setup Commands

| Command           | Description                | Usage                 |
| ----------------- | -------------------------- | --------------------- |
| `make venv`       | Create virtual environment | One-time setup        |
| `make install`    | Install dependencies       | After env creation    |
| `make dev-setup`  | Complete setup             | **Recommended start** |
| `make pre-commit` | Setup pre-commit hooks     | Quality automation    |

### Development Commands

| Command        | Description              | Usage               |
| -------------- | ------------------------ | ------------------- |
| `make run`     | Start the agent          | **Primary testing** |
| `make debug`   | Run with debug output    | Troubleshooting     |
| `make shell`   | Interactive Python shell | REPL development    |
| `make adk-web` | Launch web interface     | Web-based testing   |

### Quality Commands

| Command           | Description         | Usage              |
| ----------------- | ------------------- | ------------------ |
| `make check`      | Quick quality check | **Frequent use**   |
| `make ci`         | Full CI pipeline    | **Before commits** |
| `make fix`        | Auto-fix issues     | Code cleanup       |
| `make test`       | Run tests           | Basic testing      |
| `make test-cov`   | Tests with coverage | Coverage analysis  |
| `make test-watch` | Continuous testing  | Development mode   |

### Code Quality Commands

| Command          | Description       | Usage               |
| ---------------- | ----------------- | ------------------- |
| `make lint`      | Check code style  | Style validation    |
| `make lint-fix`  | Fix style issues  | Auto-formatting     |
| `make format`    | Format code       | Code formatting     |
| `make typecheck` | Type checking     | Type safety         |
| `make security`  | Security analysis | Security checks     |
| `make audit`     | Dependency audit  | Vulnerability check |

### Documentation Commands

| Command           | Description         | Usage          |
| ----------------- | ------------------- | -------------- |
| `make docs`       | Build documentation | Doc generation |
| `make docs-serve` | Serve docs locally  | Local preview  |
| `make docs-clean` | Clean doc build     | Reset docs     |

### Maintenance Commands

| Command             | Description          | Usage             |
| ------------------- | -------------------- | ----------------- |
| `make clean`        | Clean build files    | Cleanup           |
| `make status`       | Project health check | System status     |
| `make upgrade-deps` | Update dependencies  | Maintenance       |
| `make benchmark`    | Performance tests    | Performance check |

## 🎯 Workflow Patterns

### Quick Development Loop

For rapid iteration:

```bash
# Start watch mode for continuous testing
make test-watch

# In another terminal, work on your code
# ... edit files ...

# Periodically check overall quality
make check
```

### Feature Development Workflow

For adding new features:

```bash
# 1. Setup
git checkout -b feature/new-feature
make dev-setup

# 2. Develop
# ... implement feature ...
make check          # Frequent validation

# 3. Test thoroughly
make run            # Manual testing
make test-cov       # Automated testing

# 4. Quality assurance
make ci             # Full pipeline

# 5. Commit
git add .
git commit -m "feat: implement new feature"
git push origin feature/new-feature
```

### Bug Fix Workflow

For fixing bugs:

```bash
# 1. Reproduce
git checkout -b fix/issue-description
make run            # Reproduce the issue

# 2. Debug
make debug          # Run with debug output
make shell          # Interactive debugging

# 3. Fix and test
# ... implement fix ...
make test           # Verify fix

# 4. Validate
make ci             # Ensure no regressions

# 5. Commit
git add .
git commit -m "fix: resolve issue with weather data"
git push origin fix/issue-description
```

### Release Preparation Workflow

For preparing releases:

```bash
# 1. Quality check
make ci             # Full pipeline

# 2. Documentation
make docs           # Build docs
make docs-serve     # Review docs

# 3. Performance
make benchmark      # Performance check

# 4. Security
make audit          # Security audit

# 5. Clean build
make clean
make install
make test
```

## 🔧 Configuration

### Development Environment Variables

Copy and configure your environment:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Google Cloud Configuration
PROJECT_ID=your-development-project
LOCATION=us-central1

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
DEVELOPMENT_MODE=true

# API Keys (optional for development)
OPENWEATHER_API_KEY=your_api_key_here
```

### IDE Configuration

For VS Code, recommended settings:

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

## 🧪 Testing Strategies

### Unit Testing

```bash
# Run specific tests
pytest tests/test_tools.py -v

# Run with specific markers
pytest -m unit

# Run with coverage
make test-cov
```

### Integration Testing

```bash
# Run integration tests
pytest -m integration

# Run performance tests
pytest -m slow
```

### Manual Testing

```bash
# Interactive testing
make run

# Web interface testing
make adk-web

# Debug mode testing
make debug
```

## 📊 Quality Standards

### Code Coverage

- **Target**: 95%+ coverage
- **Check with**: `make test-cov`
- **View report**: Open `htmlcov/index.html`

### Code Quality

- **Linting**: Must pass `make lint`
- **Type checking**: Must pass `make typecheck`
- **Formatting**: Must pass `make format-check`
- **Security**: Must pass `make security`

### Performance

- **Response time**: < 2 seconds for weather queries
- **Memory usage**: Monitor with `make benchmark`

## 🚨 Troubleshooting

### Common Issues

**Tests failing after git pull:**

```bash
make clean
make install
make test
```

**Type checking errors:**

```bash
# Check specific file
mypy {{cookiecutter.package_name}}/specific_file.py

# Check with verbose output
make typecheck
```

**Import errors:**

```bash
# Reinstall in development mode
uv pip install -e .

# Check installation
make status
```

### Performance Issues

**Slow tests:**

```bash
# Run only fast tests
pytest -m "not slow"

# Profile specific tests
pytest --profile tests/test_specific.py
```

**Memory issues:**

```bash
# Run memory profiling
make benchmark
```

## 📚 Learning Resources

### Internal Documentation

- **API Reference**: `make docs-serve` → API docs
- **Architecture**: `docs/architecture.rst`
- **Contributing**: `docs/contributing.rst`

### External Resources

- **Google ADK**: [Official Documentation](https://github.com/google/agent-development-kit)
- **uv**: [Package Manager Guide](https://docs.astral.sh/uv/)
- **Python Testing**: [Pytest Documentation](https://docs.pytest.org/)

## 🎯 Best Practices

### Daily Habits

1. **Start with status**: `make status`
2. **Check frequently**: `make check` (every few commits)
3. **Test early**: `make run` (test changes immediately)
4. **Full validation**: `make ci` (before pushing)

### Code Organization

- **Small commits**: Commit early and often
- **Clear messages**: Use conventional commit format
- **Branch naming**: `feature/`, `fix/`, `docs/`
- **Documentation**: Update docs with code changes

### Quality Mindset

- **Test-driven**: Write tests for new features
- **Type safety**: Add type hints
- **Error handling**: Handle edge cases gracefully
- **Performance**: Consider response times

This workflow guide helps you maintain high productivity while ensuring code quality. Follow these patterns for efficient {{cookiecutter.project_name}} development!
