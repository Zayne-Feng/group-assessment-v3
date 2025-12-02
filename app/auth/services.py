"""
Authentication and authorization service layer.

This module provides business logic for user authentication and registration,
abstracting repository interactions and ensuring transactional integrity
for complex operations like student registration.
"""

from app.db_connection import get_db
from app.repositories.student_repository import student_repository
from app.repositories.user_repository import user_repository
from app.models.user import User # Explicitly import User model for type hinting if needed

class AuthService:
    """
    Service class for authentication-related operations.
    This class is not currently used, but could be expanded for more complex auth logic.
    """
    # Placeholder for future authentication service methods if needed.
    # The existing register_student is a standalone function.
    pass

def register_student(student_number: str, full_name: str, email: str, password: str):
    """
    Registers a new student by creating both a student record and a linked user account.

    This function operates as a transactional service:
    - It first performs pre-checks to ensure the student number and email are unique.
    - It then attempts to create the student record and the associated user account.
    - If any step fails (including pre-checks or database operations), the entire
      transaction is rolled back to prevent partial data insertion and maintain
      database consistency.

    Args:
        student_number (str): The student's unique identification number.
        full_name (str): The full name of the student.
        email (str): The student's email address, which also serves as their username.
        password (str): The plain-text password for the new user account.

    Returns:
        tuple[Student, User]: A tuple containing the created Student and User objects on success.

    Raises:
        ValueError: If the student number or email (username) already exists,
                    or if required fields for student/user creation are implicitly missing.
        Exception: If a critical database error occurs during the transaction,
                   or if an unexpected failure happens during record creation.
    """
    db = get_db() # Get the database connection for transaction management.
    
    try:
        # --- Pre-checks: Ensure uniqueness before proceeding with the transaction ---
        if student_repository.get_student_by_student_number(student_number):
            raise ValueError(f"Student number '{student_number}' already exists.")
            
        if user_repository.get_user_by_username(email):
            raise ValueError(f"Email '{email}' is already registered.")

        # --- Transactional Block: Create records ---
        # Create the student record.
        student = student_repository.create_student(
            student_number=student_number,
            full_name=full_name,
            email=email,
            course_name=None,  # Assuming course_name is not provided at initial registration.
            year_of_study=None # Assuming year_of_study is not provided at initial registration.
        )
        # Although repository methods are expected to raise exceptions on failure,
        # this check acts as a safeguard for unexpected repository behavior.
        if not student:
            raise Exception("Failed to create student record due to an unexpected repository issue.")

        # Create the user record, linking it to the newly created student.
        user = user_repository.create_user(
            username=email,
            password=password,
            role='student',
            student_id=student.id # Link the user to the student record.
        )
        # Safeguard check for user creation.
        if not user:
            raise Exception("Failed to create user record after successful student creation.")
            
        # If both student and user records are created successfully, commit the transaction.
        db.commit()
        return student, user

    except (ValueError, Exception) as e:
        # --- Error Handling: Rollback on any failure ---
        # Rollback the transaction to undo any changes made during this function call.
        db.rollback()
        # Re-raise the exception to be handled by the calling route or higher-level logic.
        raise e
