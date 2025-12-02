import pytest
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.alert_repository import alert_repository

@pytest.fixture(scope="module")
def sample_student():
    """Fixture to create a sample student for alert repository tests."""
    return student_repository.create_student(
        student_number='S_ALERT_TEST',
        full_name='Alert Test Student',
        email='alert.test@example.com',
        course_name='MSc Alert Testing',
        year_of_study=1
    )

@pytest.fixture(scope="module")
def sample_module():
    """Fixture to create a sample module for alert repository tests."""
    return module_repository.create_module(
        module_code='ALERT101',
        module_title='Alert Testing',
        credit=15,
        academic_year='2025/2026'
    )

def test_create_and_get_alert(sample_student, sample_module):
    """Tests creating and retrieving an alert."""
    new_alert = alert_repository.create_alert(
        student_id=sample_student.id,
        module_id=sample_module.id,
        week_number=5,
        reason="Test alert"
    )
    assert new_alert is not None
    fetched_alert = alert_repository.get_alert_by_id(new_alert.id)
    assert fetched_alert.reason == "Test alert"

def test_mark_alert_resolved(sample_student, sample_module):
    """Tests marking an alert as resolved."""
    alert = alert_repository.create_alert(sample_student.id, sample_module.id, 6, "To be resolved")
    assert alert.resolved is False
    
    alert_repository.mark_alert_resolved(alert.id)
    
    resolved_alert = alert_repository.get_alert_by_id(alert.id)
    assert resolved_alert.resolved is True
