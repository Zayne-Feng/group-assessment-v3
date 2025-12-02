"""
Management script for the Flask application.

This script provides command-line interface (CLI) commands for common
administrative tasks such as database initialization and data seeding.
It integrates with Flask's CLI system.
"""

import os
import sys
import click
from flask import current_app

# Add the project root to the Python path.
# This ensures that 'app' and 'utils' modules can be imported correctly
# when running commands from the project root.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from utils.seed_data import seed_data

# Create a Flask application instance for the CLI commands.
# The configuration is determined by the 'FLASK_CONFIG' environment variable,
# defaulting to 'default' (development) if not set.
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command("init-db")
def init_db_command():
    """
    CLI command to initialize the database.

    This command performs the following actions:
    1. Deletes any existing database file specified in the application configuration.
    2. Calls the `seed_data()` function to create all necessary tables and
       populate them with initial demo data.

    This is typically used to set up a fresh development or testing database.
    """
    with app.app_context():
        db_path = current_app.config['DATABASE_PATH']
        
        try:
            # Attempt to remove the existing database file to ensure a clean slate.
            if os.path.exists(db_path):
                os.remove(db_path)
                click.echo(f"Removed existing database file: {db_path}")
            
            # Execute the seeding process which creates tables and inserts data.
            seed_data()
            click.echo('Database has been initialized and seeded successfully.')
        except ConnectionError as e:
            # Handle errors specifically related to database connection.
            click.echo(f"Error: Could not connect to the database during initialization. {e}", err=True)
            current_app.logger.error(f"Database connection error during init-db: {e}")
        except FileNotFoundError:
            # Handle cases where the database file to be removed does not exist.
            click.echo(f"Warning: Database file not found at {db_path} during removal, skipping.", err=True)
        except OSError as e:
            # Handle operating system errors during file operations (e.g., permissions).
            click.echo(f"Error: Could not remove database file at {db_path}. {e}", err=True)
            current_app.logger.error(f"OS error during init-db (file removal): {e}")
        except Exception as e:
            # Catch any other unexpected errors during the initialization process.
            click.echo(f"Error: An unexpected error occurred during database initialization. {e}", err=True)
            current_app.logger.error(f"Unexpected error during init-db: {e}", exc_info=True)

@app.cli.command("seed")
def seed_command():
    """
    CLI command to seed the database with initial data.

    This command calls the `seed_data()` function to populate the database
    with demo data. It assumes the database tables are already created.
    """
    with app.app_context():
        try:
            seed_data()
            click.echo('Database has been seeded successfully.')
        except ConnectionError as e:
            # Handle errors specifically related to database connection.
            click.echo(f"Error: Could not connect to the database during seeding. {e}", err=True)
            current_app.logger.error(f"Database connection error during seed: {e}")
        except Exception as e:
            # Catch any other unexpected errors during the seeding process.
            click.echo(f"Error: An unexpected error occurred during database seeding. {e}", err=True)
            current_app.logger.error(f"Unexpected error during seed: {e}", exc_info=True)
