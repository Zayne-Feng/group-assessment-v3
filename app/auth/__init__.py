from flask import Blueprint

auth = Blueprint('auth', __name__)

# Use a relative import to load the routes within the same package
from . import routes
