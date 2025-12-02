"""
Integration tests for the Analysis Blueprint API endpoints.

This module contains tests to verify the functionality of various
analytical API routes, ensuring they correctly retrieve and process
student data insights.
"""

import json
import pytest

@pytest.fixture(scope="module")
def admin_token(client):
    """
    Fixture to obtain an authentication token for an admin user.

    Args:
        client (FlaskClient): The test client for the Flask application.

    Returns:
        str: A JWT access token for the admin user.
    """
    credentials = {
        'username': 'admin',
        'password': 'admin',
        'context': 'staff'
    }
    response = client.post('/api/auth/login', data=json.dumps(credentials), content_type='application/json')
    return json.loads(response.data)['access_token']

def test_get_students_for_analysis(client, admin_token):
    """
    Tests the GET /api/analysis/students endpoint.
    Verifies that it returns a 200 OK status and a list of students.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/students', headers=headers)
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_get_student_detail(client, admin_token):
    """
    Tests the GET /api/analysis/students/<student_id> endpoint for an existing student.
    Verifies that it returns a 200 OK status and the correct student details.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    student_id = 1 # Assuming student with ID 1 exists from seed data.
    response = client.get(f'/api/analysis/students/{student_id}', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == student_id

def test_get_nonexistent_student_detail(client, admin_token):
    """
    Tests that fetching a non-existent student detail returns 404 Not Found.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/students/99999', headers=headers)
    assert response.status_code == 404

def test_get_stress_trend(client, admin_token):
    """
    Tests the GET /api/analysis/students/<student_id>/stress-trend endpoint.
    Verifies that it returns a 200 OK status for an existing student.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    student_id = 1 # Assuming student with ID 1 exists from seed data.
    response = client.get(f'/api/analysis/students/{student_id}/stress-trend', headers=headers)
    assert response.status_code == 200
    # Further assertions could check the structure of the returned data.

def test_get_attendance_trend(client, admin_token):
    """
    Tests the GET /api/analysis/students/<student_id>/attendance-trend endpoint.
    Verifies that it returns a 200 OK status for an existing student.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    student_id = 1 # Assuming student with ID 1 exists from seed data.
    response = client.get(f'/api/analysis/students/{student_id}/attendance-trend', headers=headers)
    assert response.status_code == 200
    # Further assertions could check the structure of the returned data.

def test_get_average_attendance_for_student(client, admin_token):
    """
    Tests the GET /api/analysis/students/<student_id>/average-attendance endpoint.
    Verifies that it returns a 200 OK status and the average attendance.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    student_id = 1 # Assuming student with ID 1 exists from seed data.
    response = client.get(f'/api/analysis/students/{student_id}/average-attendance', headers=headers)
    assert response.status_code == 200
    assert 'average_attendance' in json.loads(response.data)

def test_get_grade_distribution(client, admin_token):
    """
    Tests the GET /api/analysis/grade-distribution endpoint.
    Verifies that it returns a 200 OK status and the grade distribution data.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/grade-distribution', headers=headers)
    assert response.status_code == 200
    assert 'labels' in json.loads(response.data)
    assert 'data' in json.loads(response.data)

def test_get_stress_grade_correlation(client, admin_token):
    """
    Tests the GET /api/analysis/stress-grade-correlation endpoint.
    Verifies that it returns a 200 OK status and correlation data.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/stress-grade-correlation', headers=headers)
    assert response.status_code == 200
    assert 'labels' in json.loads(response.data)
    assert 'data' in json.loads(response.data)

def test_get_dashboard_summary(client, admin_token):
    """
    Tests the GET /api/analysis/dashboard-summary endpoint.
    Verifies that it returns a 200 OK status and summary metrics.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/dashboard-summary', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_students' in data
    assert 'total_modules' in data
    assert 'pending_alerts_count' in data
    assert 'total_users' in data

def test_get_overall_attendance_rate(client, admin_token):
    """
    Tests the GET /api/analysis/overall-attendance-rate endpoint.
    Verifies that it returns a 200 OK status and the overall attendance rate.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/overall-attendance-rate', headers=headers)
    assert response.status_code == 200
    assert 'overall_attendance_rate' in json.loads(response.data)

def test_get_submission_status_distribution(client, admin_token):
    """
    Tests the GET /api/analysis/submission-status-distribution endpoint.
    Verifies that it returns a 200 OK status and submission status distribution data.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/submission-status-distribution', headers=headers)
    assert response.status_code == 200
    assert 'labels' in json.loads(response.data)
    assert 'data' in json.loads(response.data)

def test_get_high_risk_students(client, admin_token):
    """
    Tests the GET /api/analysis/high-risk-students endpoint.
    Verifies that it returns a 200 OK status and a list of high-risk students.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/high-risk-students', headers=headers)
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_get_stress_by_module(client, admin_token):
    """
    Tests the GET /api/analysis/stress-by-module endpoint.
    Verifies that it returns a 200 OK status and stress level by module data.
    """
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/api/analysis/stress-by-module', headers=headers)
    assert response.status_code == 200
    assert 'labels' in json.loads(response.data)
    assert 'data' in json.loads(response.data)
