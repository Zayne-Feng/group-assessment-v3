"""
Integration tests for the Admin Blueprint API endpoints.

This module contains a comprehensive suite of tests to verify the functionality
and access control of the administrative API routes, covering CRUD operations
for various entities like modules, students, users, enrolments, grades,
survey responses, attendance records, and submission records.
"""

import json
import pytest
from datetime import datetime

# --- Fixtures for Test Setup ---
@pytest.fixture(scope="module")
def admin_token(client):
    """
    Fixture to obtain an authentication token for an admin user.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Returns:
        str: A JWT access token for the admin user.
    """
    credentials = {'username': 'admin', 'password': 'admin', 'context': 'staff'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    return json.loads(response.data)['access_token']

@pytest.fixture(scope="module")
def course_director_token(client):
    """
    Fixture to obtain an authentication token for a course director user.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Returns:
        str: A JWT access token for the course director user.
    """
    credentials = {'username': 'course_director', 'password': 'password', 'context': 'staff'}
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    return json.loads(response.data)['access_token']

@pytest.fixture(scope="function")
def sample_student(client, admin_token):
    """
    Fixture to create and return a sample student for testing.
    The student is created via the admin API and is cleaned up after the test.

    Args:
        client (FlaskClient): The test client for the Flask application.
        admin_token (str): JWT token for an admin user.

    Returns:
        dict: The JSON response body of the created student, including its ID.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    new_student = {
        'student_number': f'S_ADMIN_{datetime.now().timestamp()}', 
        'full_name': 'Admin Test Student',
        'email': f'admin.test.student.{datetime.now().timestamp()}@example.com',
        'course_name': 'Computer Science',
        'year_of_study': 1
    }
    response = client.post('/api/admin/students', data=json.dumps(new_student), headers=headers)
    assert response.status_code == 201 # Ensure creation is successful
    return json.loads(response.data)

@pytest.fixture(scope="function")
def sample_module(client, admin_token):
    """
    Fixture to create and return a sample module for testing.
    The module is created via the admin API and is cleaned up after the test.

    Args:
        client (FlaskClient): The test client for the Flask application.
        admin_token (str): JWT token for an admin user.

    Returns:
        dict: The JSON response body of the created module, including its ID.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    new_module = {
        'module_code': f'ADMIN_{datetime.now().timestamp()}', 
        'module_title': 'Admin Test Module',
        'credit': 15,
        'academic_year': '2023/2024'
    }
    response = client.post('/api/admin/modules', data=json.dumps(new_module), headers=headers)
    assert response.status_code == 201 # Ensure creation is successful
    return json.loads(response.data)

# --- Test Suites for CRUD Operations ---
def test_module_endpoints(client, admin_token, sample_module):
    """
    Tests the full CRUD lifecycle for module endpoints.
    Verifies GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    module_id = sample_module['id']
    
    # GET single module
    response = client.get(f'/api/admin/modules/{module_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == module_id
    
    # PUT (update) module
    updated_data = {'module_title': 'Updated CRUD Module'}
    response = client.put(f'/api/admin/modules/{module_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) module
    response = client.delete(f'/api/admin/modules/{module_id}', headers=headers)
    assert response.status_code == 200

def test_student_endpoints(client, admin_token, sample_student):
    """
    Tests the full CRUD lifecycle for student endpoints.
    Verifies GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    student_id = sample_student['id']
    
    # GET single student
    response = client.get(f'/api/admin/students/{student_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == student_id
    
    # PUT (update) student
    updated_data = {'full_name': 'Updated CRUD Student'}
    response = client.put(f'/api/admin/students/{student_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) student
    response = client.delete(f'/api/admin/students/{student_id}', headers=headers)
    assert response.status_code == 200

def test_user_endpoints(client, admin_token):
    """
    Tests the full CRUD lifecycle for user endpoints.
    Verifies POST (create), GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    new_user = {'username': f'crud_user_{datetime.now().timestamp()}', 'password': 'pw', 'role': 'user'}
    
    # POST (create) user
    response = client.post('/api/admin/users', data=json.dumps(new_user), headers=headers)
    assert response.status_code == 201
    user_id = json.loads(response.data)['id']
    
    # GET single user
    response = client.get(f'/api/admin/users/{user_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == user_id
    
    # PUT (update) user
    updated_data = {'username': 'updated_crud_user'}
    response = client.put(f'/api/admin/users/{user_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) user
    response = client.delete(f'/api/admin/users/{user_id}', headers=headers)
    assert response.status_code == 200

def test_enrolment_endpoints(client, admin_token, sample_student, sample_module):
    """
    Tests the full CRUD lifecycle for enrolment endpoints.
    Verifies POST (create), GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    
    # POST (create) enrolment
    new_enrolment = {'student_id': sample_student['id'], 'module_id': sample_module['id']}
    response = client.post('/api/admin/enrolments', data=json.dumps(new_enrolment), headers=headers)
    assert response.status_code == 201
    enrolment_id = json.loads(response.data)['id']
    
    # GET single enrolment
    response = client.get(f'/api/admin/enrolments/{enrolment_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == enrolment_id
    
    # PUT (update) enrolment
    updated_data = {'enrol_date': datetime.now().isoformat()}
    response = client.put(f'/api/admin/enrolments/{enrolment_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) enrolment
    response = client.delete(f'/api/admin/enrolments/{enrolment_id}', headers=headers)
    assert response.status_code == 200

def test_grade_endpoints(client, admin_token, sample_student, sample_module):
    """
    Tests the full CRUD lifecycle for grade endpoints.
    Verifies POST (create), GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    
    # POST (create) grade
    new_grade = {'student_id': sample_student['id'], 'module_id': sample_module['id'], 'assessment_name': 'Final', 'grade': 88}
    response = client.post('/api/admin/grades', data=json.dumps(new_grade), headers=headers)
    assert response.status_code == 201
    grade_id = json.loads(response.data)['id']
    
    # GET single grade
    response = client.get(f'/api/admin/grades/{grade_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == grade_id
    
    # PUT (update) grade
    updated_data = {'grade': 90}
    response = client.put(f'/api/admin/grades/{grade_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) grade
    response = client.delete(f'/api/admin/grades/{grade_id}', headers=headers)
    assert response.status_code == 200

def test_survey_response_endpoints(client, admin_token, sample_student, sample_module):
    """
    Tests the full CRUD lifecycle for survey response endpoints.
    Verifies POST (create), GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    
    # POST (create) survey response
    new_survey = {'student_id': sample_student['id'], 'module_id': sample_module['id'], 'week_number': 1, 'stress_level': 3, 'hours_slept': 7, 'mood_comment': 'Fine'}
    response = client.post('/api/admin/survey-responses', data=json.dumps(new_survey), headers=headers)
    assert response.status_code == 201
    survey_id = json.loads(response.data)['id']
    
    # GET single survey response
    response = client.get(f'/api/admin/survey-responses/{survey_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == survey_id
    
    # PUT (update) survey response
    updated_data = {'stress_level': 5}
    response = client.put(f'/api/admin/survey-responses/{survey_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) survey response
    response = client.delete(f'/api/admin/survey-responses/{survey_id}', headers=headers)
    assert response.status_code == 200

def test_attendance_record_endpoints(client, admin_token, sample_student, sample_module):
    """
    Tests the full CRUD lifecycle for attendance record endpoints.
    Verifies POST (create), GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    
    # POST (create) attendance record
    new_record = {'student_id': sample_student['id'], 'module_id': sample_module['id'], 'week_number': 1, 'attended_sessions': 2, 'total_sessions': 2}
    response = client.post('/api/admin/attendance-records', data=json.dumps(new_record), headers=headers)
    assert response.status_code == 201
    record_id = json.loads(response.data)['id']
    
    # GET single attendance record
    response = client.get(f'/api/admin/attendance-records/{record_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == record_id
    
    # PUT (update) attendance record
    updated_data = {'attended_sessions': 1}
    response = client.put(f'/api/admin/attendance-records/{record_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) attendance record
    response = client.delete(f'/api/admin/attendance-records/{record_id}', headers=headers)
    assert response.status_code == 200

def test_submission_record_endpoints(client, admin_token, sample_student, sample_module):
    """
    Tests the full CRUD lifecycle for submission record endpoints.
    Verifies POST (create), GET (single), PUT (update), and DELETE (logical) operations.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    
    # POST (create) submission record
    new_record = {'student_id': sample_student['id'], 'module_id': sample_module['id'], 'assessment_name': 'CW1', 'due_date': datetime.now().isoformat(), 'submitted_date': None, 'is_submitted': False, 'is_late': False}
    response = client.post('/api/admin/submission-records', data=json.dumps(new_record), headers=headers)
    assert response.status_code == 201
    record_id = json.loads(response.data)['id']
    
    # GET single submission record
    response = client.get(f'/api/admin/submission-records/{record_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == record_id
    
    # PUT (update) submission record
    updated_data = {'is_submitted': True}
    response = client.put(f'/api/admin/submission-records/{record_id}', data=json.dumps(updated_data), headers=headers)
    assert response.status_code == 200
    
    # DELETE (logical delete) submission record
    response = client.delete(f'/api/admin/submission-records/{record_id}', headers=headers)
    assert response.status_code == 200

# --- Sad Path and Permission Tests ---
def test_create_endpoints_missing_fields(client, admin_token):
    """
    Tests that POST requests to create endpoints fail with 400 Bad Request
    when required fields are missing.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    
    endpoints = {
        'modules': {'module_code': 'INCOMPLETE'},
        'students': {'full_name': 'INCOMPLETE'},
        'users': {'username': 'incomplete', 'password': 'pw'},
        'enrolments': {'student_id': 1},
        'grades': {'student_id': 1, 'module_id': 1},
        'survey-responses': {'student_id': 1, 'week_number': 1},
        'attendance-records': {'student_id': 1, 'module_id': 1},
        'submission-records': {'student_id': 1, 'module_id': 1}
    }
    
    for endpoint, data in endpoints.items():
        response = client.post(f'/api/admin/{endpoint}', data=json.dumps(data), headers=headers)
        assert response.status_code == 400
        assert 'Missing required fields' in json.loads(response.data)['message']

def test_delete_nonexistent_records(client, admin_token):
    """
    Tests that DELETE requests for non-existent records return 404 Not Found.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    endpoints = [
        'modules', 'students', 'users', 'enrolments', 'grades', 
        'survey-responses', 'attendance-records', 'submission-records', 'alerts'
    ]
    for endpoint in endpoints:
        # First, ensure the record does not exist
        get_response = client.get(f'/api/admin/{endpoint}/99999', headers=headers)
        assert get_response.status_code == 404 # Expect 404 for non-existent record

        # Then, attempt to delete it
        response = client.delete(f'/api/admin/{endpoint}/99999', headers=headers)
        assert response.status_code == 404 # Expect 404 for deletion of non-existent record

def test_update_nonexistent_records(client, admin_token):
    """
    Tests that PUT requests for non-existent records return 404 Not Found.
    """
    headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
    endpoints = [
        'modules', 'students', 'users', 'enrolments', 'grades', 
        'survey-responses', 'attendance-records', 'submission-records', 'alerts'
    ]
    for endpoint in endpoints:
        response = client.put(f'/api/admin/{endpoint}/99999', data=json.dumps({'some_field': 'value'}), headers=headers)
        assert response.status_code == 404

def test_get_nonexistent_records(client, admin_token):
    """
    Tests that GET requests for non-existent records return 404 Not Found.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    endpoints = [
        'modules', 'students', 'users', 'enrolments', 'grades', 
        'survey-responses', 'attendance-records', 'submission-records', 'alerts'
    ]
    for endpoint in endpoints:
        response = client.get(f'/api/admin/{endpoint}/99999', headers=headers)
        assert response.status_code == 404

def test_unauthorized_access(client):
    """
    Tests that API endpoints require authentication and return 401 Unauthorized
    when no token is provided.
    """
    endpoints = ['/api/admin/modules', '/api/admin/students', '/api/admin/users']
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401

def test_insufficient_role_access(client, course_director_token, sample_module):
    """
    Tests that API endpoints enforce role-based access control and return 403 Forbidden
    when a user with insufficient privileges attempts an action.
    """
    headers = {'Authorization': f'Bearer {course_director_token}', 'Content-Type': 'application/json'}
    
    # course_director cannot create a module
    new_module = {'module_code': 'FAIL_TEST101', 'module_title': 'Fail Test Module'}
    response = client.post('/api/admin/modules', data=json.dumps(new_module), headers=headers)
    assert response.status_code == 403
    
    # course_director cannot delete a module
    response = client.delete(f'/api/admin/modules/{sample_module["id"]}', headers=headers)
    assert response.status_code == 403
