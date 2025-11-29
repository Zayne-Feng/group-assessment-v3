from flask import request, jsonify
from . import auth
from .services import register_student
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if UserRepository.get_user_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400

    new_user = UserRepository.create_user(username, password, role='user')
    if new_user:
        return jsonify({'message': 'Registration successful'}), 201
    
    return jsonify({'message': 'Registration failed'}), 500

@auth.route('/student/register', methods=['POST'])
def student_register():
    data = request.get_json()
    student_number = data.get('student_number')
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not all([student_number, full_name, email, password]):
        return jsonify({'message': 'All fields are required'}), 400

    try:
        student, user = register_student(student_number, full_name, email, password)
        if student and user:
            return jsonify({'message': 'Student registration successful'}), 201
        else:
            return jsonify({'message': 'Student registration failed'}), 400
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred during registration.'}), 500


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    context = data.get('context') # 'staff' or 'student'

    if not username or not password or not context:
        return jsonify({'message': 'Username, password, and context are required'}), 400

    user = UserRepository.get_user_by_username(username)

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Role validation based on context
    is_student_role = (user.role == 'student')
    
    if context == 'staff' and is_student_role:
        return jsonify({'message': 'Students must use the student login page.'}), 403 # Forbidden
        
    if context == 'student' and not is_student_role:
        return jsonify({'message': 'Staff must use the staff login page.'}), 403 # Forbidden

    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify(access_token=access_token, message='Login successful', user_role=user.role), 200
