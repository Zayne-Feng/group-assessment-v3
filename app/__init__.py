"""
Flask application package initialization.

This module contains the application factory function `create_app`,
which is responsible for creating and configuring the Flask application instance.
It initializes extensions, registers blueprints, and sets up configuration based on the environment.
"""

from flask import Flask
from flask_jwt_extended import JWTManager
from config import config
from .db_connection import init_app as init_db_connection
from utils.seed_data import seed_data
import sys # Used for exiting the application on critical startup errors.

# Initialize Flask-JWT-Extended extension globally.
# This extension provides JWT (JSON Web Token) support for authentication.
jwt = JWTManager()

def create_app(config_name='default'):
    """
    Application factory function.

    Creates and configures the Flask application instance based on the
    specified configuration environment. This function is the central
    place for setting up the application's components.

    Args:
        config_name (str): The name of the configuration to use (e.g., 'default',
                           'development', 'production', 'testing').

    Returns:
        Flask: The configured Flask application instance.

    Raises:
        ConnectionError: If a critical database connection failure occurs during
                         application initialization.
        Exception: If any other unexpected critical error occurs during
                   application initialization.
    """
    app = Flask(__name__)
    
    try:
        # Load configuration settings from the specified config object.
        app.config.from_object(config[config_name])
        # Perform any configuration-specific initialization (e.g., logging setup).
        config[config_name].init_app(app)

        # Initialize Flask extensions with the application instance.
        # init_db_connection sets up database teardown context and might raise ConnectionError.
        init_db_connection(app)  # Integrates database connection management with Flask's lifecycle.
        jwt.init_app(app) # Initializes JWT support for the application.

        # Import and register blueprints for different functional areas of the application.
        # Blueprints help in organizing the application into modular components.
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/api/auth') # Handles user authentication and authorization.

        from .analysis import analysis as analysis_blueprint
        app.register_blueprint(analysis_blueprint, url_prefix='/api/analysis') # Provides data analysis endpoints.
        
        from .admin import admin as admin_blueprint
        app.register_blueprint(admin_blueprint, url_prefix='/api/admin') # Manages administrative tasks and data.

        from .student import student as student_blueprint
        app.register_blueprint(student_blueprint, url_prefix='/api/student') # Exposes student-specific functionalities.

        # Register a CLI command for database initialization directly within the app factory.
        # This command serves as a fallback or alternative to the one defined in manage.py.
        # The manage.py version is generally preferred for consistency and robustness.
        @app.cli.command('init-db')
        def init_db_command():
            """
            CLI command to initialize the database (clear existing data, create tables, seed data).
            This command is primarily for development/testing environments.
            """
            with app.app_context():
                try:
                    seed_data()
                    print('Database initialized and seeded successfully.')
                except ConnectionError as e:
                    print(f"Error: Could not connect to the database. {e}", file=sys.stderr)
                    app.logger.error(f"Database connection error during init-db CLI: {e}")
                except Exception as e:
                    print(f"Error: An unexpected error occurred during database initialization. {e}", file=sys.stderr)
                    app.logger.error(f"Unexpected error during init-db CLI: {e}", exc_info=True)

        return app
    except ConnectionError as e:
        # Critical error handling for database connection failures during app setup.
        print(f"CRITICAL ERROR: Database connection failed during application factory setup. {e}", file=sys.stderr)
        if app.logger: # Check if logger is initialized before using it
            app.logger.critical(f"Database connection failed during app creation: {e}")
        sys.exit(1) # Terminate application startup as database is essential.
    except Exception as e:
        # Catch-all for any other critical, unexpected errors during application setup.
        print(f"CRITICAL ERROR: An unexpected error occurred during application factory setup. {e}", file=sys.stderr)
        if app.logger: # Check if logger is initialized before using it
            app.logger.critical(f"Unexpected error during app creation: {e}", exc_info=True)
        sys.exit(1) # Terminate application startup due to unrecoverable error.
