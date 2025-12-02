import pytest
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository
from app.repositories.grade_repository import grade_repository

@pytest.fixture(scope="module")
def sample_student():
    """Fixture to create a sample student for grade repository tests."""
    return student_repository.create_student(
        student_number='S_GRADE_TEST',
        full_name='Grade Test Student',
        email='grade.test@example.com',
        course_name='MSc Grade Testing',
        year_of_study=1
    )

@pytest.fixture(scope="module")
def sample_module():
    """Fixture to create a sample module for grade repository tests."""
    return module_repository.create_module(
        module_code='GRADE101',
        module_title='Grade Testing',
        credit=15,
        academic_year='2025/2026'
    )

def test_create_and_get_grade(sample_student, sample_module):
    """Tests creating and retrieving a grade."""
    new_grade = grade_repository.create_grade(sample_student.id, sample_module.id, "Final Exam", 88.5)
    assert new_grade is not None
    
    fetched_grade = grade_repository.get_grade_by_id(new_grade.id)
    assert fetched_grade.grade == 88.5
