"""
Main entry point for the Flask application.

This script initializes and runs the Flask application, handling environment
configuration and critical startup errors such as database connection failures.
It serves as the primary execution file for starting the web server.
"""

import os
import sys
from app import create_app
from flask import current_app # Import current_app for logging for consistent logging

# Create the Flask application instance based on the FLASK_CONFIG environment variable.
# If FLASK_CONFIG is not set, 'default' configuration (development) will be used.
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    # This block ensures the application runs only when the script is executed directly.
    try:
        # Attempt to acquire an application context for logging purposes.
        # This is crucial for logging critical errors that might occur before app.run() fully initializes.
        with app.app_context():
            current_app.logger.info("Attempting to start Flask application...")
        
        # Run the Flask development server.
        app.run()
    except ConnectionError as e:
        # Handle critical database connection errors during startup.
        # This error originates from app/db_connection.py if the database cannot be reached.
        print(f"CRITICAL ERROR: Database connection failed during application startup. {e}", file=sys.stderr)
        if app: # Ensure app object exists before trying to access its logger
            with app.app_context(): # Re-enter context for logging if needed
                current_app.logger.critical(f"Database connection failed during application startup: {e}")
        sys.exit(1) # Exit the application with a non-zero status code to indicate failure
    except Exception as e:
        # Catch any other unexpected critical errors during application startup.
        print(f"CRITICAL ERROR: An unexpected error occurred during application startup. {e}", file=sys.stderr)
        if app: # Ensure app object exists before trying to access its logger
            with app.app_context(): # Re-enter context for logging if needed
                current_app.logger.critical(f"Unexpected error during application startup: {e}", exc_info=True)
        sys.exit(1) # Exit the application with a non-zero status code to indicate failure
