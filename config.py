import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a hard to guess string'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_PATH = os.environ.get('DEV_DATABASE_PATH') or \
        os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = os.environ.get('TEST_DATABASE_PATH') or \
        os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or \
        os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
