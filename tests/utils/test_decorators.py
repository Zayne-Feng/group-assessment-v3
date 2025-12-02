"""
Unit tests for the custom Flask decorators defined in app.utils.decorators.

This module specifically tests the `role_required` decorator to ensure
it correctly enforces role-based access control on Flask endpoints.
"""

import pytest
import json
from flask import jsonify
from app.utils.decorators import role_required
from flask_jwt_extended import create_access_token # For creating custom tokens in tests

def test_role_required_with_single_role(app, client):
    """
    Tests the `role_required` decorator with a single role string.

    Verifies that:
    - A user with the required role can access the endpoint (200 OK).
    - A user with a different role is forbidden (403 Forbidden).
    """
    # Dynamically create a dummy endpoint protected by a single role.
    @app.route('/admin-only')
    @role_required('admin')
    def admin_only_endpoint():
        return jsonify(message="Welcome Admin!"), 200

    @app.route('/user-only')
    @role_required('user')
    def user_only_endpoint():
        return jsonify(message="Welcome User!"), 200

    # Obtain an admin token for testing.
    credentials = {'username': 'admin', 'password': 'admin', 'context': 'staff'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    admin_token = json.loads(response.data)['access_token']
    
    # Obtain a user token for testing.
    with app.app_context():
        # Create a dummy user for the test.
        from app.repositories.user_repository import user_repository
        dummy_user = user_repository.create_user('test_user_for_decorator', 'password', 'user')
        user_token = create_access_token(identity=dummy_user.id, additional_claims={"role": "user"})

    admin_headers = {'Authorization': f'Bearer {admin_token}'}
    user_headers = {'Authorization': f'Bearer {user_token}'}
    
    # Test: Admin should access admin-only endpoint.
    response = client.get('/admin-only', headers=admin_headers)
    assert response.status_code == 200
    assert 'Welcome Admin!' in json.loads(response.data)['message']
    
    # Test: Admin should NOT access user-only endpoint (admin is not 'user').
    response = client.get('/user-only', headers=admin_headers)
    assert response.status_code == 403
    assert 'Access forbidden' in json.loads(response.data)['msg']

    # Test: User should access user-only endpoint.
    response = client.get('/user-only', headers=user_headers)
    assert response.status_code == 200
    assert 'Welcome User!' in json.loads(response.data)['message']

    # Test: User should NOT access admin-only endpoint.
    response = client.get('/admin-only', headers=user_headers)
    assert response.status_code == 403
    assert 'Access forbidden' in json.loads(response.data)['msg']

def test_role_required_with_multiple_roles(app, client):
    """
    Tests the `role_required` decorator with a list of allowed roles.

    Verifies that:
    - Users with any of the required roles can access the endpoint (200 OK).
    - Users with other roles are forbidden (403 Forbidden).
    """
    @app.route('/staff-only')
    @role_required(['admin', 'course_director'])
    def staff_only_endpoint():
        return jsonify(message="Welcome Staff!"), 200

    # Obtain admin token.
    credentials_admin = {'username': 'admin', 'password': 'admin', 'context': 'staff'}
    response_admin = client.post('/api/auth/login', data=json.dumps(credentials_admin), content_type='application/json')
    admin_token = json.loads(response_admin.data)['access_token']

    # Obtain course_director token.
    credentials_cd = {'username': 'course_director', 'password': 'password', 'context': 'staff'}
    response_cd = client.post('/api/auth/login', data=json.dumps(credentials_cd), content_type='application/json')
    cd_token = json.loads(response_cd.data)['access_token']

    # Create a student user and token.
    with app.app_context():
        from app.repositories.user_repository import user_repository
        dummy_student_user = user_repository.create_user('test_student_for_decorator', 'password', 'student')
        student_token = create_access_token(identity=dummy_student_user.id, additional_claims={"role": "student"})

    admin_headers = {'Authorization': f'Bearer {admin_token}'}
    cd_headers = {'Authorization': f'Bearer {cd_token}'}
    student_headers = {'Authorization': f'Bearer {student_token}'}

    # Admin should access staff-only endpoint.
    response = client.get('/staff-only', headers=admin_headers)
    assert response.status_code == 200
    assert 'Welcome Staff!' in json.loads(response.data)['message']

    # Course Director should access staff-only endpoint.
    response = client.get('/staff-only', headers=cd_headers)
    assert response.status_code == 200
    assert 'Welcome Staff!' in json.loads(response.data)['message']

    # Student should NOT access staff-only endpoint.
    response = client.get('/staff-only', headers=student_headers)
    assert response.status_code == 403
    assert 'Access forbidden' in json.loads(response.data)['msg']

def test_role_required_no_token(client):
    """
    Tests that accessing a role-protected endpoint without any JWT token
    returns 401 Unauthorized (handled by Flask-JWT-Extended).
    """
    @client.application.route('/protected')
    @role_required('admin')
    def protected_endpoint():
        return jsonify(message="Should not see this"), 200

    response = client.get('/protected')
    assert response.status_code == 401
    assert 'Missing JWT' in json.loads(response.data)['msg']
