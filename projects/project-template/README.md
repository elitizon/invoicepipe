# ADK Project Template

> **A focused cookiecutter template that exactly replicates the `simple-adk-agent` structure for creating Google ADK agents with Vertex AI.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285f4.svg)](https://github.com/google/agent-development-kit)
[![Cookiecutter](https://img.shields.io/badge/cookiecutter-template-green.svg)](https://github.com/cookiecutter/cookiecutter)

## 🎯 What This Template Creates

This template generates an exact replica of the proven `simple-adk-agent` architecture, providing:

- ✅ **Complete Weather Assistant**: Working OpenWeatherMap integration with fallback
- ✅ **Vertex AI Only**: Hardcoded configuration for Google Cloud Vertex AI
- ✅ **Production Ready**: 97% test coverage, comprehensive error handling
- ✅ **Modern Tooling**: Ruff, MyPy, Pytest, Bandit, Pre-commit hooks
- ✅ **33+ Make Commands**: Complete development workflow automation
- ✅ **Zero Configuration**: Works immediately after generation

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **uv** package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Google Cloud Project** with Vertex AI enabled

### 1. Install Template Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install cookiecutter using uv
uv tool install cookiecutter
```

### 2. Generate Your Project

```bash
# Generate new ADK agent project
cookiecutter gh:your-org/adk-project-template

# You'll be prompted for:
# project_name [My Weather Agent]: My Travel Weather Bot
# description [An intelligent weather assistant built with Google ADK and Vertex AI]: Smart weather assistant for travel planning
# author_name [Your Name]: John Smith
# author_email [your.email@example.com]: john@company.com
# version [0.1.0]: 0.1.0
# python_version [3.11]: 3.11
```

### 3. Set Up Your Generated Project

```bash
# Navigate to your new project
cd my-travel-weather-bot

# Complete development environment setup
make dev-setup

# Configure your environment
cp .env.example .env
# Edit .env with your PROJECT_ID and LOCATION

# Run your agent
make run
```

## 📋 Template Configuration

### Required Inputs

| Variable         | Description                 | Example                                       |
| ---------------- | --------------------------- | --------------------------------------------- |
| `project_name`   | Human-readable project name | "My Travel Weather Bot"                       |
| `description`    | Project description         | "Smart weather assistant for travel planning" |
| `author_name`    | Your name                   | "John Smith"                                  |
| `author_email`   | Your email                  | "john@company.com"                            |
| `version`        | Initial version             | "0.1.0"                                       |
| `python_version` | Python version              | "3.11"                                        |

### Auto-Generated Variables

- `project_slug`: URL-safe directory name (e.g., "my-travel-weather-bot")
- `package_name`: Python package name (e.g., "my_travel_weather_bot")

## 🏗️ Generated Project Structure

```text
my-travel-weather-bot/
├── pyproject.toml              # Poetry config with exact dependencies
├── Makefile                    # 33+ development commands
├── .env.example               # Environment template
├── .gitignore                 # Python .gitignore
├── README.md                  # Project-specific documentation
├── run_agent.py               # Agent runner
├── my_travel_weather_bot/     # Main package
│   ├── __init__.py            # Package discovery for ADK CLI
│   ├── agent.py               # Agent definition with root_agent
│   ├── config.py              # Vertex AI configuration
│   ├── exceptions.py          # Custom exception hierarchy
│   └── tools.py               # Weather tools with fallback
├── tests/                     # Complete test suite (97% coverage)
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_tools.py
│   └── test_integration.py
└── docs/                      # Architecture documentation
    └── architecture.md
```

## 🛠️ Generated Project Features

### Immediate Functionality

After generation, your project includes:

- **Working weather agent** with OpenWeatherMap integration
- **Mock data fallback** when API key not configured
- **Vertex AI integration** (hardcoded, no other LLM options)
- **Complete test suite** with 97% coverage
- **Development workflow** with quality gates

### Available Commands

```bash
make dev-setup     # Complete development environment setup
make run           # Start your weather agent
make check         # Quick quality check (lint + type + test)
make test-cov      # Run tests with coverage report
make ci            # Full CI pipeline locally
make adk-web       # Launch ADK web interface
make help          # See all 33+ available commands
```

### Configuration

Your generated project uses **Vertex AI only**:

```python
# config.py (hardcoded)
GOOGLE_GENAI_USE_VERTEXAI: str = "TRUE"  # Always Vertex AI
PROJECT_ID: str | None = os.getenv("PROJECT_ID")
LOCATION: str | None = os.getenv("LOCATION", "us-central1")
```

Required environment variables:

```bash
PROJECT_ID=your-google-cloud-project-id
LOCATION=us-central1
OPENWEATHER_API_KEY=your_api_key_here  # Optional
```

## 🎯 Example Usage Workflow

```bash
# 1. Generate project
cookiecutter gh:your-org/adk-project-template

# 2. Set up development environment
cd my-weather-bot
make dev-setup

# 3. Configure environment
cp .env.example .env
# Edit .env with your PROJECT_ID

# 4. Test the agent
make run
# Try: "What's the weather in Paris?"

# 5. Development workflow
make check         # Quick validation
# ... make changes ...
make test-cov     # Run tests with coverage
make ci           # Full quality check

# 6. Launch web interface
make adk-web      # Open browser to test agent
```

## 🔧 Advanced Configuration

### Using with Different Package Managers

While the template uses Poetry by default, you can adapt it:

```bash
# With uv (recommended)
cd my-weather-bot
uv venv
uv pip install -e .

# With pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Customizing the Generated Project

After generation, you can:

1. **Modify the weather tools** in `tools.py`
2. **Add new tools** and register them in `agent.py`
3. **Customize agent instructions** in `agent.py`
4. **Add new configuration** in `config.py`

## ✅ Quality Assurance

### Generated Project Quality

Every generated project includes:

- **97% Test Coverage**: Comprehensive test suite
- **Type Safety**: Full MyPy type checking
- **Code Quality**: Ruff linting and formatting
- **Security**: Bandit security scanning
- **Documentation**: Complete README and architecture docs

### Template Validation

The template includes validation hooks that ensure:

- Valid project names (letters, numbers, hyphens, underscores)
- Valid email format
- No empty or invalid inputs

## 🚨 Troubleshooting

### Common Issues

**Template generation fails:**

```bash
# Ensure cookiecutter is installed
uv tool install cookiecutter

# Or use pip
pip install cookiecutter
```

**Generated project doesn't work:**

```bash
# Check Python version
python --version  # Should be 3.11+

# Ensure uv is installed
uv --version

# Run the setup
make dev-setup
```

**Agent fails to start:**

```bash
# Check configuration
make status

# Verify environment
cp .env.example .env
# Edit .env with your PROJECT_ID
```

### Getting Help

1. **Generated Project Issues**: Check the generated project's README.md
2. **Template Issues**: Create an issue in this repository
3. **ADK Questions**: See [Google ADK Documentation](https://github.com/google/agent-development-kit)

## 🤝 Contributing

### Improving the Template

1. Fork this repository
2. Make your changes to the template files
3. Test template generation:
   ```bash
   cookiecutter /path/to/your/template
   cd test-project
   make dev-setup && make check
   ```
4. Submit a pull request

### Template Structure

```text
adk-project-template/
├── cookiecutter.json              # Template configuration
├── hooks/                         # Validation hooks
│   ├── pre_gen_project.py         # Pre-generation validation
│   └── post_gen_project.py        # Post-generation setup
└── {{cookiecutter.project_slug}}/ # Template files
    ├── pyproject.toml             # Dependencies and tools
    ├── Makefile                   # Development commands
    └── ...                        # All template files
```

## 📚 Learn More

- **[Simple ADK Agent](https://github.com/your-org/simple-adk-agent)**: The reference implementation
- **[Google ADK](https://github.com/google/agent-development-kit)**: Official ADK documentation
- **[Cookiecutter](https://cookiecutter.readthedocs.io/)**: Template engine documentation
- **[uv](https://docs.astral.sh/uv/)**: Modern Python package manager

---

**Ready to build intelligent weather agents?** Generate your project in under 2 minutes and start building!

_Built with ❤️ using Google ADK, Cookiecutter, and modern Python development practices._
