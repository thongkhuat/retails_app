# Retail App Service

_Retail App Service is a FastAPI-based application for managing a small-scale retail system, including users, customers, products, inventory, and orders. It uses Supabase as the database and is deployed via GitHub to Fly.io._ 

## Overview

This project provides a RESTful API with endpoints for user authentication, customer management, product catalog, inventory tracking, and order processing. It’s designed to run locally or in the cloud, leveraging modern Python technologies and a PostgreSQL database hosted on Supabase.

## Downloading the Project

* Clone the repository from GitHub:
  `````bash
  git clone https://github.com/yourusername/retail-app.git
  cd retail-app
  `````

## Installing Dependencies

### Setting Up Virtual Environment (Windows Bash)

To isolate dependencies, set up a virtual environment:

* Create the virtual environment:
  `````bash
  python -m venv venv
  `````

* Activate the virtual environment:
  `````bash
  source venv/Scripts/activate
  `````

### Run tests
  `````bash
  pytest --import-mode=importlib --html=tests/reports/report.html tests/features
  `````

### Install Required Packages

Install dependencies listed in ````requirements.txt````:

* Run:
  `````bash
  pip install -r requirements.txt
  `````

## Folder Structure

Here’s the project structure:

* ````retail_app/```` - Root directory
  * ````core/```` - Core utilities and configurations
    * ````__init__.py````
    * ````config.py```` - App settings (e.g., JWT secret, database URL)
    * ````database.py```` - Database setup and session management
    * ````security.py```` - JWT authentication utilities
    * ````auth_utils.py```` - Password hashing utilities
  * ````models/```` - SQLAlchemy models
    * ````__init__.py````
    * ````db_models.py```` - Database schema definitions
  * ````schemas/```` - Pydantic schemas for validation
    * ````__init__.py````
    * ````user.py````
    * ````customer.py````
    * ````product.py````
    * ````inventory.py````
    * ````order.py````
  * ````crud/```` - CRUD operations
    * ````__init__.py````
    * ````user.py````
    * ````customer.py````
    * ````product.py````
    * ````inventory.py````
    * ````order.py````
  * ````api/```` - API endpoints
    * ````__init__.py````
    * ````deps.py```` - Dependency injection utilities
    * ````v1/```` - Versioned API endpoints
      * ````__init__.py````
      * ````user.py````
      * ````customer.py````
      * ````product.py````
      * ````inventory.py````
      * ````order.py````
  * ````main.py```` - App entry point
  * ````requirements.txt```` - Dependency list
  * ````fly.toml```` - Fly.io configuration
  * ````Procfile```` - Process definition for deployment
  * ````README.md```` - This documentation

## Technologies Used

* **FastAPI**: High-performance web framework for building APIs with Python 3.6+.
* **Uvicorn**: ASGI server to run the FastAPI app.
* **SQLAlchemy**: ORM for database interactions.
* **Supabase**: PostgreSQL-based Backend-as-a-Service for database hosting.
* **PyJWT**: Library for JWT authentication.
* **Passlib with bcrypt**: Password hashing for security.
* **psycopg2-binary**: PostgreSQL adapter for Python.
* **Fly.io**: Cloud platform for deployment.
* **GitHub Actions**: CI/CD for automated deployment.

## Local Machine Deployment Guidelines
Follow these steps to deploy the app on your local machine
* Run:
  `````bash
  uvicorn main:app
  `````
* Test:
  `````bash
  http://127.0.0.1:8000/docs
  `````