# Student Wellbeing & Academic Performance Monitoring System

This project is a prototype system designed to integrate, analyze, and visualize student engagement and wellbeing data. It features a Vue.js frontend and a Flask backend, aiming to empower educational institutions to better understand and support their students' overall health and academic success.

## Table of Contents

- [System Overview](#system-overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)

## System Overview

The **Student Wellbeing & Academic Performance Monitoring System** is a modern Web API service built with Python and Flask. It addresses a core educational challenge: a student's success is determined not just by grades, but by a combination of factors including learning engagement, mental health, and overall wellbeing.

By collecting and analyzing multi-dimensional data—such as academic grades, class attendance, assignment submissions, and self-reported stress levels—this system provides educational administrators (like Course Directors and Wellbeing Officers) with data-driven insights. The ultimate goal is to shift from a reactive to a **proactive support model**. The built-in intelligent analysis engine automatically identifies "at-risk" students, enabling staff to offer timely and targeted support, thereby enhancing the student experience and academic outcomes.

## Features

### Backend (Flask API)

-   **Unified Authentication & Authorization**: JWT-based user registration and login, with a fine-grained role-based access control (RBAC) system (`admin`, `course_director`, `wellbeing_officer`, `student`).
-   **Comprehensive Data Management (CRUD)**: Full CRUD APIs for all core entities, including students, modules, users, enrolments, grades, attendance, submissions, survey responses, and alerts.
-   **Intelligent Data Analysis**: Endpoints for a dashboard summary, grade distribution, stress-grade correlation, overall attendance rates, submission status distribution, and high-risk student identification.
-   **Alerting System**: Manages and resolves system-generated alerts related to student wellbeing.

### Frontend (Vue.js App)

-   **Intuitive User Interface**: Presents backend data through a user-friendly interface.
-   **Data Visualization**: Utilizes charts and graphs to display analytical data, turning numbers into insights.
-   **Interactive Experience**: Handles user input and actions, communicating with the backend API via Axios.
-   **State Management**: Uses Pinia for robust and centralized application state management.
-   **Client-Side Routing**: Employs Vue Router for seamless navigation and view rendering.

## Technical Architecture

The project adheres to modern software engineering best practices, featuring a clean, robust, and highly scalable architecture.

-   **Layered Architecture**:
    -   **Presentation Layer (Routes)**: Handles HTTP requests and validation.
    -   **Business Logic Layer (Services)**: Encapsulates core business logic and manages transaction boundaries.
    -   **Data Access Layer (Repositories)**: Implements the Repository Pattern, decoupling database operations from business logic.
-   **Application Factory Pattern**: Uses the `create_app()` function to instantiate and configure the Flask application, simplifying testing and environment management.
-   **Modular Design**: Leverages Flask Blueprints to separate different functional domains (`auth`, `admin`, `analysis`), reducing coupling and improving maintainability.
-   **Aspect-Oriented Programming (AOP)**: Employs custom decorators (`@role_required`) to cleanly separate cross-cutting concerns like authorization from business logic.
-   **Test-Driven Development (TDD)**: Includes a comprehensive test suite covering models, repositories, services, and APIs, ensuring code quality and correctness.

## Tech Stack

-   **Backend**: Python 3.9+, Flask, Flask-JWT-Extended, Werkzeug, python-dotenv. The data access layer is built directly on the native `sqlite3` module without an ORM.
-   **Frontend**: Vue 3, TypeScript, Vite, Pinia, Axios, Chart.js
-   **Database**: SQLite (for development and testing)
-   **Testing**: Pytest, Pytest-Mock, Pytest-Cov (Backend); Vitest, Playwright (Frontend)

## Project Structure

```
/
├── app/                  # Core Flask application
│   ├── auth/             # Authentication and authorization
│   ├── admin/            # Admin CRUD functionalities
│   ├── analysis/         # Data analysis endpoints
│   ├── student/          # Student-specific endpoints
│   ├── models/           # Data model definitions
│   ├── repositories/     # Data access layer (Repository Pattern)
│   └── utils/            # App-specific utilities (e.g., decorators)
├── frontend/vue-project/ # Vue.js frontend application
├── tests/                # Backend Pytest test suite
├── utils/                # Project-level utilities (e.g., seed_data.py)
├── .venv/                # Python virtual environment
├── app.py                # Flask application entry point
├── config.py             # Environment-specific configurations
├── manage.py             # Defines custom CLI commands (e.g., init-db)
├── requirements.txt      # Backend Python dependencies
└── package.json          # Frontend Node.js dependencies
```

## Local Development Setup

### Prerequisites

-   Python 3.9+
-   Node.js 18+
-   An IDE like PyCharm or VS Code is recommended.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 2. Backend Setup

```bash
# 1. Create and activate a Python virtual environment
python -m venv .venv
# On Windows
.\.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Set the FLASK_APP environment variable
# On Windows PowerShell
$env:FLASK_APP="manage.py"
# On macOS/Linux
export FLASK_APP=manage.py

# 4. Initialize the database (creates tables and seeds initial data)
# This will delete the old database file (if it exists) and create a fresh one.
flask init-db
```

### 3. Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend/vue-project

# 2. Install frontend dependencies
npm install
```

*Note: The Vite development server is pre-configured with a proxy to the Flask backend to avoid CORS issues. No extra configuration is needed.*

## Running the Project

You need to run the backend and frontend servers concurrently in two separate terminals.

1.  **Run the Backend (Flask)**:
    -   Ensure your Python virtual environment is activated.
    -   From the project root directory, run:
        ```bash
        python manage.py run
        ```
    -   The backend will start on `http://127.0.0.1:5000`.

2.  **Run the Frontend (Vue)**:
    -   Open a new terminal.
    -   Navigate to the `frontend/vue-project` directory.
    -   Run:
        ```bash
        npm run dev
        ```
    -   The frontend development server will start. Open the URL shown in the terminal (usually `http://localhost:5173`).

## Running Tests

-   **Backend Tests**:
    ```bash
    # From the project root, with the virtual environment activated
    pytest --cov=app
    ```

-   **Frontend Tests**:
    ```bash
    # Navigate to the frontend/vue-project directory
    npm run test:unit  # For unit tests
    npm run test:e2e   # For end-to-end tests
    ```
