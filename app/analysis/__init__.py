from flask import Blueprint

analysis = Blueprint('analysis', __name__)

# Use a relative import to load the routes within the same package
from . import routes
