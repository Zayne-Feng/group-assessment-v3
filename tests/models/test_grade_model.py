import pytest
from app.models.grade import Grade
from datetime import datetime

def test_grade_initialization():
    """Tests the initialization of the Grade model."""
    grade = Grade(id=1, student_id=2, module_id=3, assessment_name='Exam', grade=88.0)
    assert grade.id == 1
    assert grade.assessment_name == 'Exam'
    assert grade.grade == 88.0

def test_grade_to_dict():
    """Tests the to_dict method of the Grade model."""
    now = datetime.now()
    grade = Grade(id=1, student_id=2, created_at=now)
    grade_dict = grade.to_dict()
    assert grade_dict['id'] == 1
    assert grade_dict['student_id'] == 2
    assert grade_dict['created_at'] == now.isoformat()

def test_grade_from_row():
    """Tests the from_row class method of the Grade model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'assessment_name': 'Exam',
        'grade': 88.0,
        'is_active': 1,
        'created_at': now_iso
    }
    grade = Grade.from_row(row)
    assert grade.id == 1
    assert grade.grade == 88.0
    assert grade.created_at.isoformat() == now_iso
