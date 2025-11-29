from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import student
from app.repositories.user_repository import user_repository # Import the instance
from app.repositories.student_repository import student_repository # Import the instance
from app.utils.decorators import role_required

@student.route('/me', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_profile():
    """
    Returns the profile of the currently logged-in student.
    """
    current_user_id = get_jwt_identity()
    user = user_repository.get_user_by_id(current_user_id) # Use the instance
    
    if not user or not user.student_id:
        return jsonify({"message": "Student profile not found for this user."}), 404
        
    student_profile = student_repository.get_student_by_id(user.student_id) # Use the instance
    
    if not student_profile:
        return jsonify({"message": "Student profile data is missing."}), 404
        
    return jsonify(student_profile.to_dict()), 200
