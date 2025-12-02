"""
Module for Flask decorators, primarily for access control and authentication.

This module provides custom decorators that can be applied to Flask view functions
to enforce specific requirements, such as role-based access control, leveraging
Flask-JWT-Extended for authentication context.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
    """
    A decorator to protect Flask endpoints, allowing access only to users with specified roles.

    This decorator performs two main checks:
    1. It verifies the presence and validity of a JWT (JSON Web Token) in the request.
       If the JWT is missing, invalid, or expired, Flask-JWT-Extended's error
       handlers will automatically intercept and return a 401 Unauthorized response.
    2. It extracts the user's role from the validated JWT claims and checks if
       that role is among the list of allowed roles for the decorated endpoint.

    Args:
        roles (str or list): A single role string (e.g., 'admin') or a list of
                             role strings (e.g., ['admin', 'course_director'])
                             that are permitted to access the decorated endpoint.

    Returns:
        Callable: A decorator function that wraps the protected endpoint.
                  The wrapped function will either execute the original view
                  function or return a 403 Forbidden response.
    """
    # Ensure the 'roles' argument is always treated as a list for consistent processing.
    if not isinstance(roles, list):
        roles = [roles]

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify the JWT in the request. If invalid, Flask-JWT-Extended handles the 401 response.
            verify_jwt_in_request()
            
            # Retrieve the claims (payload) from the verified JWT.
            claims = get_jwt()
            
            # Extract the 'role' claim from the JWT payload.
            user_role = claims.get("role")
            
            # Check if the user's role exists and is authorized to access this endpoint.
            if user_role and user_role in roles:
                # If the user has an allowed role, proceed to execute the original view function.
                return fn(*args, **kwargs)
            else:
                # If the user's role is missing or not authorized, return a 403 Forbidden response.
                return jsonify({"msg": f"Access forbidden: One of roles {roles} required"}), 403
        return wrapper
    return decorator
