import pytest
from app import create_app

@pytest.fixture(scope='module')
def app():
    """
    Creates and configures a new Flask app instance for each test module.
    The 'testing' configuration is used to enable testing-specific features.
    """
    # Create a Flask app configured for testing
    app = create_app('testing')
    
    # Establish an application context
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    """
    Creates a test client for the Flask app.
    This client can be used to make requests to the application's endpoints.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """
    Creates a CLI test runner for the Flask app.
    This can be used to invoke Flask CLI commands like 'init-db'.
    """
    return app.test_cli_runner()

@pytest.fixture(scope='module', autouse=True)
def init_database(runner):
    """
    An auto-use fixture to initialize the database at the start of the test session.
    This ensures that all tests run against a clean, seeded database.
    """
    # Invoke the 'init-db' command.
    result = runner.invoke(args=['init-db'])
    
    # Check if the command executed successfully
    assert 'Initialized the database.' in result.output
    
    yield # The tests will run after this point
