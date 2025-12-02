import pytest
from app.repositories.student_repository import student_repository

def test_create_and_get_student():
    """
    Tests that a student can be created and then retrieved from the database.
    """
    new_student = student_repository.create_student(
        student_number='S5555',
        full_name='Repo Test Student',
        email='repo.student@example.com',
        course_name='MSc Testing',
        year_of_study=1
    )
    assert new_student is not None
    assert new_student.id is not None
    
    fetched_student = student_repository.get_student_by_id(new_student.id)
    assert fetched_student is not None
    assert fetched_student.full_name == 'Repo Test Student'
    assert fetched_student.student_number == 'S5555'

def test_get_student_by_student_number():
    """
    Tests that a student can be retrieved by their student number.
    """
    student_repository.create_student(
        student_number='S6666',
        full_name='Repo Test Student 2',
        email='repo.student2@example.com',
        course_name='MSc Testing',
        year_of_study=1
    )
    
    fetched_student = student_repository.get_student_by_student_number('S6666')
    assert fetched_student is not None
    assert fetched_student.full_name == 'Repo Test Student 2'

def test_hard_delete_student(app):
    """
    Tests that a student can be permanently deleted from the database.
    """
    # Create a student to permanently delete
    student_to_delete = student_repository.create_student(
        student_number='S_HARD_DELETE',
        full_name='To Be Hard Deleted',
        email='hard.delete@example.com',
        course_name='MSc Deletion',
        year_of_study=1
    )
    student_id = student_to_delete.id
    
    # Perform a hard delete
    delete_success = student_repository.delete_hard(student_id)
    assert delete_success is True
    
    # Verify the student is completely gone, even when including inactive
    fetched_student = student_repository.get_student_by_id(student_id, include_inactive=True)
    assert fetched_student is None
