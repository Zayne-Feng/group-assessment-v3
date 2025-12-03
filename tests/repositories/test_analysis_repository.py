"""
Unit and Integration tests for the AnalysisRepository.

This module contains tests to verify the correctness of complex analytical
queries and data aggregation logic implemented in the `AnalysisRepository`.
It covers both mocked unit tests for specific logic and integration tests
that interact with a seeded database.
"""

import pytest
from app.repositories.analysis_repository import analysis_repository
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.grade_repository import grade_repository
from app.repositories.survey_response_repository import survey_response_repository

# --- Unit Tests: Mocking the _execute_query method ---

def test_get_high_risk_students_low_attendance(mocker):
    """
    Unit test to verify `get_high_risk_students` correctly identifies
    a high-risk student due to low attendance.

    Mocks the underlying `_execute_query` calls to simulate database responses.
    """
    # Simulate database responses for low attendance, no low grades, no high stress.
    mocker.patch.object(analysis_repository, '_execute_query', side_effect=[
        [{'id': 1, 'full_name': 'John Doe', 'avg_attendance': 60}], # Low attendance query result
        [], # Low grades query result
        []  # High stress query result
    ])
    high_risk_students = analysis_repository.get_high_risk_students(attendance_threshold=70)
    assert len(high_risk_students) == 1
    assert high_risk_students[0]['id'] == 1
    assert "Low attendance" in high_risk_students[0]['reason']

def test_get_high_risk_students_multiple_reasons(mocker):
    """
    Unit test to verify `get_high_risk_students` correctly identifies
    a high-risk student with multiple risk factors (low attendance and low grades).

    Mocks the underlying `_execute_query` calls to simulate database responses.
    """
    # Simulate database responses for low attendance, low grades, no high stress.
    mocker.patch.object(analysis_repository, '_execute_query', side_effect=[
        [{'id': 2, 'full_name': 'Jane Smith', 'avg_attendance': 50}], # Low attendance query result
        [{'id': 2, 'full_name': 'Jane Smith', 'avg_grade': 35}],     # Low grades query result
        [] # High stress query result
    ])
    high_risk_students = analysis_repository.get_high_risk_students(attendance_threshold=70, grade_threshold=40)
    assert len(high_risk_students) == 1
    assert high_risk_students[0]['id'] == 2
    assert "Low attendance" in high_risk_students[0]['reason']
    assert "Low average grade" in high_risk_students[0]['reason']

def test_get_high_risk_students_no_risk(mocker):
    """
    Unit test to verify `get_high_risk_students` returns an empty list
    when no students meet the high-risk criteria.

    Mocks the underlying `_execute_query` calls to simulate empty database responses.
    """
    # Simulate empty database responses for all risk queries.
    mocker.patch.object(analysis_repository, '_execute_query', return_value=[])
    high_risk_students = analysis_repository.get_high_risk_students()
    assert len(high_risk_students) == 0

# --- Integration Tests: Interacting with a seeded database ---

def test_get_dashboard_summary_integration():
    """
    Integration test for `get_dashboard_summary`.

    Verifies that the dashboard summary data is correctly retrieved,
    relying on the initial seed data provided by the test setup.
    """
    summary = analysis_repository.get_dashboard_summary()
    assert 'total_students' in summary
    assert 'total_modules' in summary
    assert 'pending_alerts_count' in summary
    assert 'total_users' in summary
    # Assert that seed data was loaded and counts are non-zero.
    assert summary['total_students'] > 0
    assert summary['total_users'] > 0
    # Specific values could be asserted if seed data is deterministic.

def test_get_stress_grade_correlation_integration():
    """
    Integration test for `get_stress_grade_correlation`.

    Verifies that correlation data can be generated from newly created
    student, module, survey, and grade records.
    """
    # Create test data to ensure a calculable correlation.
    student = student_repository.create_student('S_CORR_1', 'Corr Student', 'corr@test.com', 'MSc Corr', 1)
    module = module_repository.create_module('CORR101', 'Correlation', 10, '2025')
    survey_response_repository.create_survey_response(student.id, module.id, 1, 4, 7, "OK") # High stress
    grade_repository.create_grade(student.id, module.id, "Exam", 75) # Good grade

    correlation_data = analysis_repository.get_stress_grade_correlation()
    assert 'labels' in correlation_data
    assert 'data' in correlation_data
    assert isinstance(correlation_data['data'], list)
    
    # Verify that the newly created student's data is present in the correlation results.
    student_in_data = any(d['name'] == 'Corr Student' for d in correlation_data['data'])
    assert student_in_data

def test_get_grade_distribution_integration():
    """
    Integration test for `get_grade_distribution`.

    Verifies that grade distribution is correctly calculated based on
    newly created student and grade records across different bands.
    """
    # Create test students with grades in different bands.
    student1 = student_repository.create_student('S_DIST_1', 'Distinction Student', 'dist1@test.com', 'MSc Dist', 1)
    student2 = student_repository.create_student('S_DIST_2', 'Fail Student', 'dist2@test.com', 'MSc Dist', 1)
    module = module_repository.create_module('DIST101', 'Distribution', 10, '2025')
    grade_repository.create_grade(student1.id, module.id, "Exam", 65) # Example: Distinction band
    grade_repository.create_grade(student2.id, module.id, "Exam", 35) # Example: Fail band

    distribution = analysis_repository.get_grade_distribution()
    assert 'labels' in distribution
    assert 'data' in distribution
    assert distribution['labels'] == ['Fail (<40)', 'Pass (40-49)', 'Merit (50-59)', 'Distinction (60-69)', 'Excellent (70+)']
    
    # Find the indices for 'Fail' and 'Distinction' bands.
    fail_index = distribution['labels'].index('Fail (<40)')
    distinction_index = distribution['labels'].index('Distinction (60-69)')

    # Assert that the counts for our new students are reflected (at least 1 in each band).
    assert distribution['data'][fail_index] >= 1
    assert distribution['data'][distinction_index] >= 1
