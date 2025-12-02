import pytest
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.enrolment_repository import enrolment_repository

@pytest.fixture(scope="module")
def sample_student():
    """Fixture to create a sample student for enrolment repository tests."""
    return student_repository.create_student(
        student_number='S_ENROL_TEST',
        full_name='Enrolment Test Student',
        email='enrol.test@example.com',
        course_name='MSc Enrolment Testing',
        year_of_study=1
    )

@pytest.fixture(scope="module")
def sample_module():
    """Fixture to create a sample module for enrolment repository tests."""
    return module_repository.create_module(
        module_code='ENROL101',
        module_title='Enrolment Testing',
        credit=15,
        academic_year='2025/2026'
    )

def test_create_and_get_enrolment(sample_student, sample_module):
    """Tests creating and retrieving an enrolment."""
    new_enrolment = enrolment_repository.create_enrolment(sample_student.id, sample_module.id)
    assert new_enrolment is not None
    
    fetched_enrolment = enrolment_repository.get_enrolment_by_id(new_enrolment.id)
    assert fetched_enrolment.student_id == sample_student.id
    assert fetched_enrolment.module_id == sample_module.id
