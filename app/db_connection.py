import sqlite3
import os
from flask import current_app, g

def get_db():
    """
    Establishes a connection to the SQLite database and returns the connection object.
    The connection is stored in Flask's application context (g) for reuse.
    """
    if 'db' not in g:
        db_path = current_app.config['DATABASE_PATH']
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # Return rows as dict-like objects
    return g.db

def close_db(e=None):
    """
    Closes the database connection if it exists in the application context.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Registers the close_db function with the Flask app context.
    """
    app.teardown_appcontext(close_db)
