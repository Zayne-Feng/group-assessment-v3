"""
Authentication and authorization routes for the Flask application.

This module defines API endpoints related to user registration and login,
handling different user contexts (staff and student) and issuing JWTs.
"""

from flask import request, jsonify, current_app
from . import auth
from .services import register_student
from app.repositories.user_repository import user_repository
from flask_jwt_extended import create_access_token # Used to create JWTs for authenticated users.

@auth.route('/register', methods=['POST'])
def register():
    """
    Handles general user registration for staff or non-student users.

    Expects JSON payload with 'username' and 'password'.
    Checks for existing usernames and creates a new user with a default 'user' role.

    Args:
        None (data is extracted from request.get_json()).

    Returns:
        Response: JSON response indicating success or failure of registration.
                  - 201 Created: Registration successful.
                  - 400 Bad Request: Missing fields or username already exists.
                  - 500 Internal Server Error: Unexpected server-side error.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate required input fields.
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    try:
        # Check if a user with the given username already exists to prevent duplicates.
        if user_repository.get_user_by_username(username):
            return jsonify({'message': 'Username already exists'}), 400

        # Attempt to create a new user in the database.
        new_user = user_repository.create_user(username, password, role='user')
        if new_user:
            return jsonify({'message': 'Registration successful'}), 201
        else:
            # This branch indicates a logical failure in user creation within the repository
            # that did not raise an explicit exception.
            current_app.logger.error(f"User creation failed for username: {username} but no exception was raised.")
            return jsonify({'message': 'Registration failed for an unknown reason'}), 500
    except Exception as e:
        # Catch any unexpected exceptions during the registration process (e.g., database errors).
        current_app.logger.error(f"Error during registration: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred during registration.'}), 500

@auth.route('/student/register', methods=['POST'])
def student_register():
    """
    Handles student-specific registration, creating both a student record and a linked user account.

    Expects JSON payload with 'student_number', 'full_name', 'email', and 'password'.
    Leverages the `register_student` service for transactional creation.

    Args:
        None (data is extracted from request.get_json()).

    Returns:
        Response: JSON response indicating success or failure of student registration.
                  - 201 Created: Student registration successful.
                  - 400 Bad Request: Missing fields or validation errors from service layer.
                  - 500 Internal Server Error: Unexpected server-side error.
    """
    data = request.get_json()
    student_number = data.get('student_number')
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    # Validate all required fields are present.
    if not all([student_number, full_name, email, password]):
        return jsonify({'message': 'All fields are required'}), 400

    try:
        # Call the service layer function to handle transactional student and user creation.
        student, user = register_student(student_number, full_name, email, password)
        if student and user:
            return jsonify({'message': 'Student registration successful'}), 201
        else:
            # This branch indicates a logical failure in student creation within the service
            # that did not raise an explicit exception.
            current_app.logger.error(f"Student registration failed for email: {email} but no exception was raised.")
            return jsonify({'message': 'Student registration failed for an unknown reason'}), 500
    except ValueError as e:
        # Catch specific validation errors (e.g., student number or email already exists)
        # raised by the service layer.
        return jsonify({'message': str(e)}), 400 # 400 Bad Request for client-side validation issues.
    except Exception as e:
        # Catch any unexpected exceptions during student registration (e.g., database errors).
        current_app.logger.error(f"Error during student registration: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred during registration.'}), 500


@auth.route('/login', methods=['POST'])
def login():
    """
    Handles user login, authenticates credentials, and issues a JWT access token.

    Expects JSON payload with 'username', 'password', and 'context' ('staff' or 'student').
    Performs role-based context validation to ensure correct login flow.

    Args:
        None (data is extracted from request.get_json()).

    Returns:
        Response: JSON response containing the access token and user role on success,
                  or an error message on failure.
                  - 200 OK: Login successful, returns JWT.
                  - 400 Bad Request: Missing fields.
                  - 401 Unauthorized: Invalid credentials.
                  - 403 Forbidden: Role context mismatch.
                  - 500 Internal Server Error: Unexpected server-side error.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    context = data.get('context') # Expected to be 'staff' or 'student'.

    # Validate all required input fields.
    if not username or not password or not context:
        return jsonify({'message': 'Username, password, and context are required'}), 400

    try:
        # Retrieve user from the database based on username.
        user = user_repository.get_user_by_username(username)

        # Authenticate user credentials.
        if not user or not user.check_password(password):
            return jsonify({'message': 'Invalid username or password'}), 401

        # Perform role-based context validation.
        # This ensures that staff users log in via staff portal and students via student portal.
        is_student_role = (user.role == 'student')
        
        if context == 'staff' and is_student_role:
            return jsonify({'message': 'Students must use the student login page.'}), 403 # Forbidden
            
        if context == 'student' and not is_student_role:
            return jsonify({'message': 'Staff must use the staff login page.'}), 403 # Forbidden

        # If authentication and role context are valid, create and return a JWT access token.
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        return jsonify(access_token=access_token, message='Login successful', user_role=user.role), 200
    except Exception as e:
        # Catch any unexpected exceptions during the login process (e.g., database errors).
        current_app.logger.error(f"Error during login: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred during login.'}), 500
