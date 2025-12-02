"""
Database connection management for the Flask application.

This module is responsible for establishing and managing the lifecycle of
the SQLite database connection within the Flask application context.
It ensures that a single database connection is used per request and
is properly closed when the request finishes.

Note on Error Handling:
This module's primary responsibility is to provide and manage the database
connection's lifecycle. It specifically handles errors that occur during
the *establishment* of the database connection (e.g., file not found,
permission issues). Errors during actual database *operations* (e.g.,
executing queries) are delegated to the repository layer
(see `app/repositories/base_repository.py`) to maintain separation of concerns.
"""

import sqlite3
import os
from flask import current_app, g

def get_db():
    """
    Establishes and retrieves the application's configured database connection.

    The database connection is stored in Flask's `g` object (application context
    global) to ensure that:
    1. A new connection is created only once per request.
    2. The same connection is reused if `get_db()` is called multiple times
       within the same request.

    The connection is configured to return rows as `sqlite3.Row` objects,
    allowing column access by name.

    Returns:
        sqlite3.Connection: The active database connection object.

    Raises:
        ConnectionError: If the database file cannot be opened or accessed,
                         indicating a critical failure to establish connection.
    """
    # Check if the database connection already exists in the current application context.
    if 'db' not in g:
        db_path = current_app.config['DATABASE_PATH']
        try:
            # Attempt to establish a new SQLite database connection.
            g.db = sqlite3.connect(
                db_path,
                detect_types=sqlite3.PARSE_DECLTYPES # Automatically parse types like datetime.
            )
            # Configure the connection to return rows as dict-like objects.
            g.db.row_factory = sqlite3.Row
        except sqlite3.OperationalError as e:
            # Log a critical error if the database connection fails.
            current_app.logger.critical(f"Failed to connect to database at {db_path}: {e}")
            # Re-raise a custom ConnectionError to signal a critical failure to the caller.
            raise ConnectionError(f"Could not connect to the database: {e}") from e
        
    return g.db

def close_db(e=None):
    """
    Closes the database connection at the end of the request or application context.

    This function is registered with Flask's `teardown_appcontext` to be
    automatically called when the application context is torn down, ensuring
    that database connections are properly released.

    Args:
        e (Exception, optional): An exception that might have occurred during
                                 the request processing. Defaults to None.
    """
    # Retrieve the database connection from the application context, if it exists.
    db = g.pop('db', None)

    # If a database connection was established, close it.
    if db is not None:
        db.close()
        # current_app.logger.debug("Database connection closed.") # Optional: for verbose logging

def init_app(app):
    """
    Registers database-related functions with the Flask application.

    This function is called by the application factory (`create_app`) to
    integrate database lifecycle management with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    # Register `close_db` to be called automatically when the application
    # context ends, ensuring database connections are always closed.
    app.teardown_appcontext(close_db)
