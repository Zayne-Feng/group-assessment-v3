import pytest
from app.models.enrolment import Enrolment
from datetime import datetime, date

def test_enrolment_initialization():
    """Tests the initialization of the Enrolment model."""
    enrolment = Enrolment(id=1, student_id=2, module_id=3)
    assert enrolment.id == 1
    assert enrolment.student_id == 2
    assert isinstance(enrolment.enrol_date, date)

def test_enrolment_to_dict():
    """Tests the to_dict method of the Enrolment model."""
    now = datetime.now()
    enrolment = Enrolment(id=1, student_id=2, created_at=now)
    enrolment_dict = enrolment.to_dict()
    assert enrolment_dict['id'] == 1
    assert enrolment_dict['student_id'] == 2
    assert isinstance(enrolment_dict['enrol_date'], str)
    assert enrolment_dict['created_at'] == now.isoformat()

def test_enrolment_from_row():
    """Tests the from_row class method of the Enrolment model."""
    now_iso = datetime.now().isoformat()
    today_iso = date.today().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'enrol_date': today_iso,
        'is_active': 1,
        'created_at': now_iso
    }
    enrolment = Enrolment.from_row(row)
    assert enrolment.id == 1
    assert enrolment.student_id == 2
    assert enrolment.enrol_date.isoformat() == today_iso
    assert enrolment.created_at.isoformat() == now_iso
