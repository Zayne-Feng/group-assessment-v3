from app.db_connection import get_db
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository

def register_student(student_number, full_name, email, password):
    """
    Registers a new student by creating a student record and a corresponding user record.
    Raises ValueError if the student number or email (username) already exists.
    """
    db = get_db()
    
    # Check for existing student number
    if StudentRepository.get_student_by_student_number(student_number):
        raise ValueError(f"Student number {student_number} already exists.")
        
    # Check for existing user (email)
    if UserRepository.get_user_by_username(email):
        raise ValueError(f"Email {email} is already registered.")

    try:
        # Create student record
        student = StudentRepository.create_student(
            student_number=student_number,
            full_name=full_name,
            email=email,
            course_name=None,  # Assuming course_name is not provided at registration
            year_of_study=None # Assuming year_of_study is not provided at registration
        )
        if not student:
            raise Exception("Failed to create student record.")

        # Create user record, linking it to the new student
        user = UserRepository.create_user(
            username=email,
            password=password,
            role='student',
            student_id=student.id # Pass the student_id to the user creation
        )
        if not user:
            # If user creation fails, we should roll back the student creation.
            # As we are not using a transaction block, we manually delete the student.
            StudentRepository.delete_student_hard(student.id) # A hard delete is needed here
            raise Exception("Failed to create user record.")
            
        db.commit()
        return student, user

    except Exception as e:
        db.rollback()
        raise e
