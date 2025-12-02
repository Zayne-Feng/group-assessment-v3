"""
Integration tests for the Student Blueprint API endpoints.

This module contains tests to verify the functionality and access control
of student-specific API routes, primarily focusing on retrieving personal
profile information.
"""

import json
import pytest
from flask_jwt_extended import create_access_token
from app.repositories.user_repository import user_repository
from app.repositories.student_repository import student_repository

@pytest.fixture(scope="module")
def student_token(client):
    """
    Fixture to obtain an authentication token for a student user.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Returns:
        str: A JWT access token for the student user.
    """
    # Register a student user first to get a valid student token.
    student_data = {"student_number": "S_TEST_01", "full_name": "Test Student User", "email": "student.test@example.com", "password": "password123"}
    client.post('/api/auth/student/register', data=json.dumps(student_data), content_type='application/json')
    
    # Log in as the registered student to get the token.
    credentials = {'username': 'student.test@example.com', 'password': 'password123', 'context': 'student'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    return json.loads(response.data)['access_token']

def test_get_my_profile_unauthorized(client):
    """
    Tests that accessing /api/student/me without a JWT returns 401 Unauthorized.
    """
    response = client.get('/api/student/me')
    assert response.status_code == 401

def test_get_my_profile_authorized(client, student_token):
    """
    Tests successful retrieval of a student's own profile via /api/student/me.
    Verifies a 200 OK status and correct student number.
    """
    headers = {'Authorization': f'Bearer {student_token}'}
    response = client.get('/api/student/me', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['student_number'] == 'S_TEST_01'

def test_get_my_profile_user_not_found(client, app):
    """
    Tests that accessing /api/student/me with a token for a non-existent user ID
    (but with 'student' role claim) returns 404 Not Found.
    """
    with app.app_context():
        # Create a token for a non-existent user ID.
        non_existent_user_token = create_access_token(identity=99999, additional_claims={"role": "student"})
    
    headers = {'Authorization': f'Bearer {non_existent_user_token}'}
    response = client.get('/api/student/me', headers=headers)
    assert response.status_code == 404
    assert "Student profile not found" in response.get_json()['message']

def test_get_my_profile_user_no_student_id(client, app):
    """
    Tests that accessing /api/student/me with a token for a user that has
    no associated student_id (and a non-'student' role) returns 403 Forbidden.
    """
    with app.app_context():
        # Create a user with role 'user' and no student_id.
        dummy_user = user_repository.create_user('no_student_id_user', 'password', 'user', student_id=None)
        # Create a token for this user, with role 'user'.
        no_student_id_token = create_access_token(identity=dummy_user.id, additional_claims={"role": "user"})
    
    headers = {'Authorization': f'Bearer {no_student_id_token}'}
    response = client.get('/api/student/me', headers=headers)
    # The @role_required('student') decorator will block this request, returning 403.
    assert response.status_code == 403 
    assert "Access forbidden" in response.get_json()['msg']
