"""
Configuration management for the Flask application.

This module defines different configuration classes for various environments
(development, testing, production) to manage settings like secret keys,
database paths, and debug modes.
"""

import os

# Determine the base directory of the application for relative path calculations.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class.
    Contains common settings applicable to all environments.
    """
    # Secret key for Flask sessions and other security-related functions.
    # Retrieved from environment variable or defaults to a hardcoded string (for development).
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a hard to guess string'
    
    # Secret key for Flask-JWT-Extended to sign JWTs.
    # Retrieved from environment variable or defaults to a hardcoded string (for development).
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'
    
    @staticmethod
    def init_app(app):
        """
        Initializes the application with any specific configurations needed after app creation.
        This base method does nothing, but can be overridden by subclasses.

        Args:
            app (Flask): The Flask application instance.
        """
        pass

class DevelopmentConfig(Config):
    """
    Development environment configuration.
    Enables debug mode and sets the development database path.
    """
    DEBUG = True # Enable debug mode for detailed error messages and auto-reloading.
    
    # Path to the SQLite database file for the development environment.
    # Retrieved from environment variable or defaults to 'data-dev.sqlite' in the base directory.
    DATABASE_PATH = os.environ.get('DEV_DATABASE_PATH') or \
        os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    """
    Testing environment configuration.
    Enables testing mode and sets the testing database path.
    """
    TESTING = True # Enable testing mode, which suppresses error catching during request handling.
    
    # Path to the SQLite database file for the testing environment.
    # Retrieved from environment variable or defaults to 'data-test.sqlite' in the base directory.
    DATABASE_PATH = os.environ.get('TEST_DATABASE_PATH') or \
        os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    """
    Production environment configuration.
    Sets the production database path. Debug mode is typically disabled in production.
    """
    # Path to the SQLite database file for the production environment.
    # Retrieved from environment variable or defaults to 'data.sqlite' in the base directory.
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or \
        os.path.join(basedir, 'data.sqlite')

# Dictionary mapping configuration names to their respective configuration classes.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # 'default' uses the development configuration.
}
