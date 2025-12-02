"""
Integration tests for the Authentication Blueprint API endpoints.

This module contains tests to verify the functionality of user registration
and login processes, including handling valid/invalid credentials and
role-based context validation.
"""

import json
import pytest

def test_register(client):
    """
    Tests successful user registration via POST /api/auth/register.
    Verifies a 201 Created status and a success message.
    """
    new_user = {'username': 'testuser_auth', 'password': 'testpassword'}
    response = client.post('/api/auth/register', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 201
    assert 'Registration successful' in response.get_json()['message']

def test_register_missing_fields(client):
    """
    Tests user registration failure when required fields are missing.
    Verifies a 400 Bad Request status.
    """
    incomplete_user = {'username': 'incomplete_user'}
    response = client.post('/api/auth/register', data=json.dumps(incomplete_user), content_type='application/json')
    assert response.status_code == 400
    assert 'Username and password are required' in response.get_json()['message']

def test_login(client):
    """
    Tests successful user login with valid credentials via POST /api/auth/login.
    Verifies a 200 OK status and the presence of an access token.
    """
    credentials = {'username': 'admin', 'password': 'admin', 'context': 'staff'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_invalid_password(client):
    """
    Tests user login failure with an invalid password.
    Verifies a 401 Unauthorized status.
    """
    credentials = {'username': 'admin', 'password': 'wrongpassword', 'context': 'staff'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    assert response.status_code == 401
    assert 'Invalid username or password' in response.get_json()['message']

def test_login_missing_fields(client):
    """
    Tests user login failure when required fields (username, password, context) are missing.
    Verifies a 400 Bad Request status.
    """
    incomplete_credentials = {'username': 'admin'} # Missing password and context
    response = client.post('/api/auth/login', data=json.dumps(incomplete_credentials), content_type='application/json')
    assert response.status_code == 400
    assert 'Username, password, and context are required' in response.get_json()['message']

def test_login_student_as_staff(client):
    """
    Tests that a student user cannot log in via the 'staff' context.
    Verifies a 403 Forbidden status.
    """
    # First, register a student user.
    student_data = {"student_number": "S_AUTH_TEST", "full_name": "Auth Test Student", "email": "auth.student@example.com", "password": "password123"}
    client.post('/api/auth/student/register', data=json.dumps(student_data), content_type='application/json')
    
    # Attempt to log in as this student using the 'staff' context.
    credentials = {'username': 'auth.student@example.com', 'password': 'password123', 'context': 'staff'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    assert response.status_code == 403
    assert 'Students must use the student login page.' in response.get_json()['message']

def test_login_staff_as_student(client):
    """
    Tests that a staff user (admin) cannot log in via the 'student' context.
    Verifies a 403 Forbidden status.
    """
    credentials = {'username': 'admin', 'password': 'admin', 'context': 'student'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    assert response.status_code == 403
    assert 'Staff must use the staff login page.' in response.get_json()['message']
