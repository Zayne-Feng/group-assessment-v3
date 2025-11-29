from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import student
from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository
from app.utils.decorators import role_required

@student.route('/me', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_profile():
    """
    Returns the profile of the currently logged-in student.
    """
    current_user_id = get_jwt_identity()
    user = UserRepository.get_user_by_id(current_user_id)
    
    if not user or not user.student_id:
        return jsonify({"message": "Student profile not found for this user."}), 404
        
    student_profile = StudentRepository.get_student_by_id(user.student_id)
    
    if not student_profile:
        return jsonify({"message": "Student profile data is missing."}), 404
        
    return jsonify(student_profile.to_dict()), 200
