import pytest
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.stress_event_repository import stress_event_repository

@pytest.fixture(scope="module")
def sample_student():
    """Fixture to create a sample student for stress event repository tests."""
    return student_repository.create_student(
        student_number='S_STRESS_TEST',
        full_name='Stress Test Student',
        email='stress.test@example.com',
        course_name='MSc Stress Testing',
        year_of_study=1
    )

@pytest.fixture(scope="module")
def sample_module():
    """Fixture to create a sample module for stress event repository tests."""
    return module_repository.create_module(
        module_code='STRESS101',
        module_title='Stress Testing',
        credit=15,
        academic_year='2025/2026'
    )

def test_create_and_get_stress_event(sample_student, sample_module):
    """
    Tests that a stress event can be created and then retrieved from the database.
    """
    new_event = stress_event_repository.create_stress_event(
        student_id=sample_student.id,
        module_id=sample_module.id,
        survey_response_id=None,
        week_number=8,
        stress_level=5,
        cause_category="academic",
        description="Final exams pressure",
        source="manual"
    )
    assert new_event is not None
    assert new_event.id is not None
    
    fetched_event = stress_event_repository.get_stress_event_by_id(new_event.id)
    assert fetched_event is not None
    assert fetched_event.cause_category == "academic"
    assert fetched_event.stress_level == 5

def test_update_stress_event(sample_student, sample_module):
    """
    Tests that a stress event can be updated in the database.
    """
    # Create an event to update
    event_to_update = stress_event_repository.create_stress_event(
        student_id=sample_student.id,
        module_id=sample_module.id,
        survey_response_id=None,
        week_number=9,
        stress_level=4,
        cause_category="personal",
        description="Initial description",
        source="manual"
    )
    
    # Update the event
    updated_event = stress_event_repository.update_stress_event(
        event_id=event_to_update.id,
        student_id=sample_student.id,
        module_id=sample_module.id,
        survey_response_id=None,
        week_number=9,
        stress_level=3,
        cause_category="personal",
        description="Updated description",
        source="manual_update"
    )
    assert updated_event is not None
    assert updated_event.description == "Updated description"
    assert updated_event.stress_level == 3
    
    # Verify by fetching again
    fetched_event = stress_event_repository.get_stress_event_by_id(event_to_update.id)
    assert fetched_event.description == "Updated description"
