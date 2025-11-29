from flask import Flask
from flask_jwt_extended import JWTManager
from config import config
from .db_connection import init_app as init_db_connection, get_db
from utils.seed_data import seed_data

jwt = JWTManager()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    init_db_connection(app)
    jwt.init_app(app)

    # Import and register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .analysis import analysis as analysis_blueprint
    app.register_blueprint(analysis_blueprint, url_prefix='/api/analysis')
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')

    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/api/student')

    # Register CLI command for database initialization
    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        with app.app_context():
            seed_data()
            print('Initialized the database.')

    return app
