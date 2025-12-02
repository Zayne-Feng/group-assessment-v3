"""
Authentication Blueprint initialization.

This module creates and configures the Flask Blueprint for the authentication
section of the application. It registers the blueprint and imports its
associated routes to make them available to the Flask application.
"""

from flask import Blueprint

# Create a Blueprint instance for the 'auth' module.
# Blueprints help in organizing a Flask application into smaller, reusable components.
auth = Blueprint('auth', __name__)

# Import the routes defined within the 'auth' blueprint.
# This ensures that the routes are registered with the blueprint.
from . import routes
