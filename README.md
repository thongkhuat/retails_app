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
  uvicorn main:app --reload
  `````

## Intranet Deployment Guidelines

Follow these steps to deploy the app using GitHub with Fly.io, connected to a Supabase database.

### Prerequisites

* **Supabase Database**:
  * Create a project on ````supabase.com````.
  * Initialize the database with ````init_retail_db.sql```` (see below).
  * Get the connection string: ````postgresql://postgres:[YOUR_PASSWORD]*db.[PROJECT_REF].supabase.co:5432/postgres````.
* **GitHub Repository**: Push your code to a repo (e.g., ````https://github.com/yourusername/retail-app````).
* **Fly.io Account**: Sign up at ````fly.io```` and install ````flyctl````.

### Initialize Supabase Database

* Run in Supabase SQL Editor or via ````psql````:
  `````bash
  psql -h db.[PROJECT_REF].supabase.co -U postgres -d postgres -f init_retail_db.sql
  `````

### Configure Fly.io

* Initialize Fly.io app:
  `````bash
  flyctl init
  `````
  * App name: e.g., ````retail-app-yourname````.
  * Region: e.g., ````sin```` (Singapore).
* Edit ````fly.toml```` (see above).
* Create ````Procfile```` (see above).

### Set Environment Variables

* Set Supabase connection:
  `````bash
  flyctl secrets set DATABASE_URL="postgresql://postgres:[YOUR_PASSWORD]*db.[PROJECT_REF].supabase.co:5432/postgres"
  `````

### Deploy Manually (Initial Setup)

* Deploy to Fly.io:
  `````bash
  flyctl deploy
  `````
* Check deployment:
  `````bash
  flyctl status
  `````
* Access: ````https://retail-app-yourname.fly.dev/docs````.

### Automate with GitHub Actions

* Create ````.github/workflows/deploy.yml````:
  `````yaml
  name: Deploy to Fly.io
  on:
    push:
      branches:
        - main
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout*v3
        - name: Set up Flyctl
          uses: superfly/flyctl-actions/setup-flyctl*master
        - name: Deploy to Fly.io
          run: flyctl deploy --remote-only
          env:
            FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
  `````
* Add secrets in GitHub:
  * Go to "Settings" > "Secrets and variables" > "Actions".
  * Add ````FLY_API_TOKEN```` (from ````flyctl auth token````).
  * Add ````DATABASE_URL```` (Supabase connection string).

### Test the Deployment

* Visit ````https://retail-app-yourname.fly.dev/docs````.
* Test endpoints:
  * ````POST /login```` with ````{"username": "admin", "password": "12345678"}````.
  * ````POST /user/```` to create a new user.