from flask import request, jsonify
from . import auth
from app.models.user import User
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Use static method
    if UserRepository.get_user_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400

    # Use static method
    new_user = UserRepository.create_user(username, password, role='user')
    if new_user:
        return jsonify({'message': 'Registration successful'}), 201
    
    return jsonify({'message': 'Registration failed'}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Use static method
    user = UserRepository.get_user_by_username(username)

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create access token
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify(access_token=access_token, message='Login successful', user_role=user.role), 200
