import os
import sys
import click
import sqlite3
from flask import current_app

# Add the project root to the Python path to resolve import issues
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.db_connection import get_db, close_db
from utils.seed_data import seed_data

# Create an app instance for the commands
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# We no longer have SQLAlchemy models to pass to the shell context directly
# @app.shell_context_processor
# def make_shell_context():
#     """Makes additional variables available in the Flask shell."""
#     return dict(db=get_db(), User=User, Student=Student, Module=Module, Enrolment=Enrolment,
#                 AttendanceRecord=AttendanceRecord, SubmissionRecord=SubmissionRecord,
#                 Grade=Grade, SurveyResponse=SurveyResponse, StressEvent=StressEvent, Alert=Alert)

@app.cli.command("init-db")
@click.confirmation_option(prompt='Are you sure you want to drop and re-create the database?')
def init_db_command():
    """Drops and re-creates the database, then seeds it with data."""
    with app.app_context():
        db_path = current_app.config['DATABASE_PATH']
        
        # Remove existing db file if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            click.echo(f"Removed existing database file: {db_path}")

        # Create tables and seed data using the new sqlite3 approach
        seed_data() # seed_data now handles table creation and data insertion
        
    click.echo('Database has been initialized and seeded.')

@app.cli.command("seed")
def seed_command():
    """Seeds the database with initial data."""
    with app.app_context():
        seed_data()
    click.echo('Database has been seeded.')
