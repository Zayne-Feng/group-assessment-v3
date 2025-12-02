import pytest
from app.models.student import Student
from datetime import datetime

def test_student_initialization():
    """Tests the initialization of the Student model."""
    student = Student(id=1, student_number='S123', full_name='John Doe', email='john@test.com', course_name='CS', year_of_study=1)
    assert student.id == 1
    assert student.full_name == 'John Doe'

def test_student_to_dict():
    """Tests the to_dict method of the Student model."""
    now = datetime.now()
    student = Student(id=1, full_name='John Doe', created_at=now)
    student_dict = student.to_dict()
    assert student_dict['id'] == 1
    assert student_dict['full_name'] == 'John Doe'
    assert student_dict['created_at'] == now.isoformat()

def test_student_from_row():
    """Tests the from_row class method of the Student model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_number': 'S123',
        'full_name': 'John Doe',
        'email': 'john@test.com',
        'course_name': 'CS',
        'year_of_study': 1,
        'is_active': 1,
        'created_at': now_iso
    }
    student = Student.from_row(row)
    assert student.id == 1
    assert student.full_name == 'John Doe'
    assert student.created_at.isoformat() == now_iso
