from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
    """
    Decorator to restrict access to endpoints based on user roles.
    Accepts a single role string or a list of role strings.
    """
    if not isinstance(roles, list):
        roles = [roles] # Convert single role to a list for consistent processing

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request() # Verify JWT is present and valid
            claims = get_jwt() # Get the claims from the JWT
            
            user_role = claims.get("role")
            
            if user_role and user_role in roles:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": f"Access forbidden: One of roles {roles} required"}), 403 # Forbidden
        return wrapper
    return decorator
