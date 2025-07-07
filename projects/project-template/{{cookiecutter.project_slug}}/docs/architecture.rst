Architecture
============

{{cookiecutter.project_name}} Architecture - Intelligent Weather Assistant
===========================================================================

A production-ready AI weather agent architecture that demonstrates intelligent conversation, robust error handling, and seamless API integration using Google ADK.

🚀 Quick Architecture Overview
------------------------------

**Core Flow**: User asks → ADK processes → Agent selects weather tool → Returns intelligent response

.. code-block:: bash

   # Architecture in action
   User: "What's the weather in Tokyo?"
   ADK Framework → root_agent → get_weather_forecast() → OpenWeatherMap API → Smart Response

**Key Design Principles:**

- **Single Responsibility**: One weather tool, one job, done well
- **Graceful Degradation**: Real API → Mock data fallback
- **User-Focused**: Always provides helpful responses
- **Vertex AI Only**: Hardcoded to use Google Cloud Vertex AI

🏗️ System Components
--------------------

Core Components
~~~~~~~~~~~~~~~

Agent (``{{cookiecutter.package_name}}.agent``)
   The main agent factory that creates and configures the weather assistant using Google ADK.

Configuration (``{{cookiecutter.package_name}}.config``)
   Centralized configuration management with Vertex AI hardcoded setup and validation.

Tools (``{{cookiecutter.package_name}}.tools``)
   Weather forecasting tools with OpenWeatherMap integration and mock data fallback.

Exceptions (``{{cookiecutter.package_name}}.exceptions``)
   Custom exception hierarchy for proper error handling throughout the application.

🔧 Configuration Management
---------------------------

The configuration system is designed to be simple and robust:

**Vertex AI Configuration (Hardcoded)**
   - ``GOOGLE_GENAI_USE_VERTEXAI``: Always set to "TRUE"
   - ``PROJECT_ID``: Required Google Cloud Project ID
   - ``LOCATION``: Google Cloud location (defaults to "us-central1")

**Weather API Configuration**
   - ``OPENWEATHER_API_KEY``: Optional OpenWeatherMap API key
   - Falls back to mock data when not configured

🌤️ Weather Tool Architecture
----------------------------

The weather tool follows a robust pattern:

1. **Input Validation**: Sanitize and validate user inputs
2. **API Integration**: Attempt real weather data retrieval
3. **Fallback Mechanism**: Use mock data if API fails
4. **Response Formatting**: Return structured, user-friendly data

🎯 Development Workflow
-----------------------

The project includes a comprehensive development workflow:

**Quality Gates**
   - Ruff linting and formatting
   - MyPy type checking
   - Pytest with 97% coverage target
   - Pre-commit hooks

**Make Commands**
   - ``make dev-setup``: Complete environment setup
   - ``make check``: Quick quality verification
   - ``make test-cov``: Tests with coverage
   - ``make docs``: Generate documentation

🚀 Deployment Considerations
----------------------------

**Authentication**
   Uses Google Cloud Application Default Credentials (ADC)

**Environment Variables**
   Minimal configuration required - just PROJECT_ID and LOCATION

**Scalability**
   Stateless design allows for easy horizontal scaling

**Monitoring**
   Built-in logging and error handling for production monitoring
