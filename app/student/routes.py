"""
Student Blueprint routes for student-specific functionalities.

This module defines API endpoints that allow authenticated students to
access their personal profile and related data within the system.
"""

from flask import jsonify, current_app # Import current_app for logging
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import student
from app.repositories.user_repository import user_repository
from app.repositories.student_repository import student_repository
from app.utils.decorators import role_required

@student.route('/me', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_profile():
    """
    Retrieves the profile of the currently logged-in student.

    This endpoint is protected and requires a valid JWT for a user with the 'student' role.
    It fetches the user's details based on the JWT identity, then finds the associated
    student profile.

    Returns:
        Response: JSON response containing the student's profile data on success,
                  or an error message on failure.
                  - 200 OK: Successfully retrieved student profile.
                  - 404 Not Found: Student profile not found for the user.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        # Get the user ID from the JWT token, which represents the currently logged-in user.
        current_user_id = get_jwt_identity()
        
        # Fetch the user record from the database using the user ID.
        user = user_repository.get_user_by_id(current_user_id)
        
        # Check if the user exists and if they are linked to a student profile.
        # A user with a 'student' role must have a valid student_id.
        if not user or not user.student_id:
            current_app.logger.warning(f"Student profile not found for user ID: {current_user_id} (user.student_id is None or user not found).")
            return jsonify({"message": "Student profile not found for this user."}), 404
            
        # Fetch the detailed student profile using the student_id obtained from the user record.
        student_profile = student_repository.get_student_by_id(user.student_id)
        
        # Double-check if the student profile data itself is missing or inactive.
        if not student_profile:
            current_app.logger.warning(f"Student profile data missing or inactive for student ID: {user.student_id} (linked to user ID: {current_user_id}).")
            return jsonify({"message": "Student profile data is missing or inactive."}), 404
            
        # Return the student profile as a JSON response.
        return jsonify(student_profile.to_dict()), 200
        
    except Exception as e:
        # Catch any unexpected exceptions (e.g., database errors from repositories).
        current_app.logger.error(f"Error getting student profile for user ID {get_jwt_identity()}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred while retrieving the profile.'}), 500
