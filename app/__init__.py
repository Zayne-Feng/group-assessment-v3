from flask import Flask
from flask_jwt_extended import JWTManager
from config import config
from .db_connection import init_app as init_db_connection # Import the init_app function from db_connection

# db = SQLAlchemy() # Remove SQLAlchemy instance
jwt = JWTManager()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # db.init_app(app) # Remove SQLAlchemy initialization
    init_db_connection(app) # Initialize the sqlite3 db connection management
    jwt.init_app(app)

    # Import and register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .analysis import analysis as analysis_blueprint
    app.register_blueprint(analysis_blueprint, url_prefix='/analysis')
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
