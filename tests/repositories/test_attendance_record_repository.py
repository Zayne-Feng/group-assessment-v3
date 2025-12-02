import pytest
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.attendance_record_repository import attendance_record_repository

@pytest.fixture(scope="module")
def sample_student():
    """Fixture to create a sample student for attendance repository tests."""
    return student_repository.create_student(
        student_number='S_ATTEND_TEST',
        full_name='Attendance Test Student',
        email='attend.test@example.com',
        course_name='MSc Attendance Testing',
        year_of_study=1
    )

@pytest.fixture(scope="module")
def sample_module():
    """Fixture to create a sample module for attendance repository tests."""
    return module_repository.create_module(
        module_code='ATTEND101',
        module_title='Attendance Testing',
        credit=15,
        academic_year='2025/2026'
    )

def test_create_and_get_attendance_record(sample_student, sample_module):
    """Tests creating and retrieving an attendance record."""
    new_record = attendance_record_repository.create_attendance_record(sample_student.id, sample_module.id, 3, 1, 2)
    assert new_record is not None
    
    fetched_record = attendance_record_repository.get_attendance_record_by_id(new_record.id)
    assert fetched_record.attendance_rate == 0.5
