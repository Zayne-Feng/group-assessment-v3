"""
Unit tests for the Authentication Service layer.

This module contains tests to verify the business logic and transactional
integrity of the `AuthService` functions, particularly `register_student`.
It uses mocking to isolate the service layer from direct database interactions.
"""

import pytest
from app.auth.services import register_student
from app.models.student import Student
from app.models.user import User
from app.repositories.student_repository import student_repository
from app.repositories.user_repository import user_repository

# --- Unit Tests for Auth Service ---

def test_register_student_success(mocker):
    """
    Tests the successful execution of the `register_student` service function.

    Verifies that both student and user records are created and linked,
    and that the database transaction is committed.
    """
    # Mock repository methods to simulate a clean database state (no existing student/user).
    mocker.patch.object(user_repository, 'get_user_by_username', return_value=None)
    mocker.patch.object(student_repository, 'get_student_by_student_number', return_value=None)
    
    # Mock the creation methods to return successful (mock) objects.
    mock_student = Student(id=1, student_number='S12345', full_name='Test Student', email='test@example.com')
    mock_user = User(id=1, username='test@example.com', role='student', student_id=1)
    mocker.patch.object(student_repository, 'create_student', return_value=mock_student)
    mocker.patch.object(user_repository, 'create_user', return_value=mock_user)
    
    # Mock the database commit method, as it's called within the service.
    mocker.patch('app.db_connection.get_db').return_value.commit = mocker.MagicMock()
    mocker.patch('app.db_connection.get_db').return_value.rollback = mocker.MagicMock() # Also mock rollback

    student, user = register_student('S12345', 'Test Student', 'test@example.com', 'password')

    assert student is not None
    assert user is not None
    assert student.student_number == 'S12345'
    assert user.username == 'test@example.com'
    assert user.student_id == student.id
    # Verify that commit was called and rollback was not.
    mocker.patch('app.db_connection.get_db').return_value.commit.assert_called_once()
    mocker.patch('app.db_connection.get_db').return_value.rollback.assert_not_called()

def test_register_student_existing_student_number(mocker):
    """
    Tests `register_student` failure when the provided student number already exists.

    Verifies that a `ValueError` is raised with the correct message.
    """
    # Mock the student repository to simulate that the student number already exists.
    mocker.patch.object(student_repository, 'get_student_by_student_number', return_value=Student(id=1, student_number='S12345'))
    
    # Mock db.rollback() as it would be called in the service's exception handler.
    mocker.patch('app.db_connection.get_db').return_value.rollback = mocker.MagicMock()
    mocker.patch('app.db_connection.get_db').return_value.commit = mocker.MagicMock()

    with pytest.raises(ValueError, match="Student number 'S12345' already exists."):
        register_student('S12345', 'Test Student', 'test@example.com', 'password')
    
    # Verify that rollback was called and commit was not.
    mocker.patch('app.db_connection.get_db').return_value.rollback.assert_called_once()
    mocker.patch('app.db_connection.get_db').return_value.commit.assert_not_called()


def test_register_student_existing_email(mocker):
    """
    Tests `register_student` failure when the provided email (username) already exists.

    Verifies that a `ValueError` is raised with the correct message.
    """
    # Mock repositories to simulate a clean student number but an existing username.
    mocker.patch.object(student_repository, 'get_student_by_student_number', return_value=None)
    mocker.patch.object(user_repository, 'get_user_by_username', return_value=User(id=1, username='test@example.com'))

    # Mock db.rollback() as it would be called in the service's exception handler.
    mocker.patch('app.db_connection.get_db').return_value.rollback = mocker.MagicMock()
    mocker.patch('app.db_connection.get_db').return_value.commit = mocker.MagicMock()

    with pytest.raises(ValueError, match="Email 'test@example.com' is already registered."):
        register_student('S12345', 'Test Student', 'test@example.com', 'password')
    
    # Verify that rollback was called and commit was not.
    mocker.patch('app.db_connection.get_db').return_value.rollback.assert_called_once()
    mocker.patch('app.db_connection.get_db').return_value.commit.assert_not_called()
