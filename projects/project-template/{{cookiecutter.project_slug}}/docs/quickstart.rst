Quick Start Guide
=================

This guide will help you get started with {{cookiecutter.project_name}} quickly.

Installation
------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.11 or higher
- pip or uv for package management

Using pip
~~~~~~~~~

.. code-block:: bash

   pip install {{cookiecutter.project_slug}}

Using uv (recommended)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   uv add {{cookiecutter.project_slug}}

Basic Usage
-----------

Setting Up Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

First, create a configuration file or set environment variables:

.. code-block:: bash

   # Create a .env file
   echo "AGENT_NAME={{cookiecutter.package_name}}" > .env
   echo "LOG_LEVEL=INFO" >> .env

Basic Agent Usage
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from {{cookiecutter.package_name}} import Agent
   from {{cookiecutter.package_name}}.config import Config
   
   # Load configuration
   config = Config()
   
   # Create agent instance
   agent = Agent(config)
   
   # Run the agent
   try:
       result = agent.run("What's the weather like today?")
       print(f"Agent response: {result}")
   except Exception as e:
       print(f"Error: {e}")

Command Line Usage
~~~~~~~~~~~~~~~~~~

Run the agent directly from the command line:

.. code-block:: bash

   # Start the interactive agent
   python run_agent.py
   
   # Or with uv
   uv run python run_agent.py

Configuration Options
---------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set these environment variables for proper configuration:

.. code-block:: bash

   # Google Cloud Configuration (Required for Vertex AI)
   export PROJECT_ID=your-google-cloud-project-id
   export LOCATION=us-central1
   
   # Weather API Configuration (Optional)
   export OPENWEATHER_API_KEY=your_api_key_here
   
   # Application Settings
   export APP_NAME={{cookiecutter.package_name}}
   export LOG_LEVEL=INFO

Configuration File
~~~~~~~~~~~~~~~~~~

Alternatively, use a ``.env`` file:

.. code-block:: dotenv

   # Google Cloud Configuration
   PROJECT_ID=your-google-cloud-project-id
   LOCATION=us-central1
   
   # Weather API Configuration
   OPENWEATHER_API_KEY=your_api_key_here
   
   # Application Settings
   APP_NAME={{cookiecutter.package_name}}
   DEBUG=false
   LOG_LEVEL=INFO

Google Cloud Setup
------------------

Authentication
~~~~~~~~~~~~~~

For development, use Application Default Credentials:

.. code-block:: bash

   # Install Google Cloud CLI
   curl https://sdk.cloud.google.com | bash
   
   # Authenticate
   gcloud auth application-default login
   
   # Set your project
   gcloud config set project YOUR_PROJECT_ID

For production, use a service account:

.. code-block:: bash

   # Set service account key path
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

Enable Required APIs
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Enable Vertex AI API
   gcloud services enable aiplatform.googleapis.com

Examples
--------

Weather Queries
~~~~~~~~~~~~~~~

The agent can handle various weather-related queries:

.. code-block:: python

   from {{cookiecutter.package_name}}.agent import root_agent
   
   # Current weather
   response = root_agent.run("What's the weather in Paris?")
   print(response)
   
   # Weather forecast
   response = root_agent.run("Will it rain tomorrow in London?")
   print(response)
   
   # Travel planning
   response = root_agent.run("Should I bring an umbrella to Tokyo this week?")
   print(response)

Interactive Usage
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from google.adk.runners import Runner
   from google.adk.sessions import InMemorySessionService
   from {{cookiecutter.package_name}}.agent import root_agent
   
   async def interactive_session():
       session_service = InMemorySessionService()
       runner = Runner(agent=root_agent, session_service=session_service)
       
       while True:
           user_input = input("You: ")
           if user_input.lower() in ['quit', 'exit']:
               break
               
           response = await runner.run(
               user_id="demo_user",
               session_id="demo_session",
               user_input=user_input
           )
           print(f"Agent: {response}")
   
   # Run the interactive session
   asyncio.run(interactive_session())

Development Setup
-----------------

For development work:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/{{cookiecutter.author_name}}/{{cookiecutter.project_slug}}.git
   cd {{cookiecutter.project_slug}}
   
   # Set up development environment
   make dev-setup
   
   # Run tests
   make test
   
   # Start the agent
   make run

Testing Your Setup
------------------

Verify Installation
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check if the package is installed correctly
   python -c "from {{cookiecutter.package_name}} import root_agent; print('✅ Installation successful')"

Test Basic Functionality
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run the test suite
   make test
   
   # Or with pytest directly
   pytest tests/

Check Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Verify configuration
   python -c "from {{cookiecutter.package_name}}.config import Config; print('✅ OK' if Config.is_configured() else '⚠️ Needs setup')"

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Error:**

.. code-block:: bash

   # Ensure the package is installed
   pip install -e .
   # Or with uv
   uv pip install -e .

**Configuration Error:**

.. code-block:: bash

   # Check your .env file
   cat .env
   
   # Verify Google Cloud authentication
   gcloud auth list

**API Errors:**

.. code-block:: bash

   # Check if APIs are enabled
   gcloud services list --enabled | grep aiplatform

Getting Help
~~~~~~~~~~~~

- **Documentation**: Run ``make docs-serve`` for local docs
- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions in GitHub Discussions

Next Steps
----------

Now that you have {{cookiecutter.project_name}} running:

1. **Explore the examples** in the ``examples/`` directory
2. **Read the full documentation** with ``make docs-serve``
3. **Customize the agent** by modifying ``{{cookiecutter.package_name}}/agent.py``
4. **Add new tools** in ``{{cookiecutter.package_name}}/tools.py``
5. **Contribute** to the project (see Contributing Guide)

For more detailed information, see the complete documentation.
