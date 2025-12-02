import pytest
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.submission_record_repository import submission_record_repository
from datetime import datetime

@pytest.fixture(scope="module")
def sample_student():
    """Fixture to create a sample student for submission repository tests."""
    return student_repository.create_student(
        student_number='S_SUBMIT_TEST',
        full_name='Submission Test Student',
        email='submit.test@example.com',
        course_name='MSc Submission Testing',
        year_of_study=1
    )

@pytest.fixture(scope="module")
def sample_module():
    """Fixture to create a sample module for submission repository tests."""
    return module_repository.create_module(
        module_code='SUBMIT101',
        module_title='Submission Testing',
        credit=15,
        academic_year='2025/2026'
    )

def test_create_and_get_submission_record(sample_student, sample_module):
    """Tests creating and retrieving a submission record."""
    due_date = datetime.now().isoformat()
    new_record = submission_record_repository.create_submission_record(sample_student.id, sample_module.id, "Coursework 1", due_date, None, False, False)
    assert new_record is not None
    
    fetched_record = submission_record_repository.get_submission_record_by_id(new_record.id)
    assert fetched_record.assessment_name == "Coursework 1"
