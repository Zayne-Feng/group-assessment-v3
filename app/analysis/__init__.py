"""
Analysis Blueprint initialization.

This module creates and configures the Flask Blueprint for the data analysis
section of the application. It registers the blueprint and imports its
associated routes to make them available to the Flask application.
"""

from flask import Blueprint

# Create a Blueprint instance for the 'analysis' module.
# Blueprints help in organizing a Flask application into smaller, reusable components.
analysis = Blueprint('analysis', __name__)

# Import the routes defined within the 'analysis' blueprint.
# This ensures that the routes are registered with the blueprint.
from . import routes
