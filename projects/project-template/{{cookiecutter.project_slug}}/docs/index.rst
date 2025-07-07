{{cookiecutter.project_name}} Documentation
=================================

Welcome to {{cookiecutter.project_name}}'s documentation!

{{cookiecutter.description}}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api
   architecture
   contributing
   development-workflow

Quick Start
-----------

1. Install dependencies:

   .. code-block:: bash

      make dev-setup

2. Configure your environment:

   .. code-block:: bash

      cp .env.example .env
      # Edit .env with your PROJECT_ID and LOCATION

3. Run the agent:

   .. code-block:: bash

      make run

Features
--------

* **Vertex AI Integration**: Hardcoded to use Google Cloud Vertex AI
* **Weather Forecasting**: Real-time weather data with OpenWeatherMap
* **Fallback Support**: Mock data when API is unavailable
* **Production Ready**: 97% test coverage, comprehensive error handling
* **Modern Development**: Full development workflow with quality gates

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
