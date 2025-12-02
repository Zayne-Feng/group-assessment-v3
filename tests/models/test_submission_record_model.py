import pytest
from app.models.submission_record import SubmissionRecord
from datetime import datetime

def test_submission_record_initialization():
    """Tests the initialization of the SubmissionRecord model."""
    record = SubmissionRecord(id=1, student_id=2, module_id=3, assessment_name='CW1', is_submitted=True)
    assert record.id == 1
    assert record.assessment_name == 'CW1'
    assert record.is_submitted is True

def test_submission_record_to_dict():
    """Tests the to_dict method of the SubmissionRecord model."""
    now = datetime.now()
    record = SubmissionRecord(id=1, student_id=2, created_at=now, due_date=now)
    record_dict = record.to_dict()
    assert record_dict['id'] == 1
    assert record_dict['student_id'] == 2
    assert record_dict['created_at'] == now.isoformat()
    assert record_dict['due_date'] == now.isoformat()

def test_submission_record_from_row():
    """Tests the from_row class method of the SubmissionRecord model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'assessment_name': 'CW1',
        'due_date': now_iso,
        'submitted_date': None,
        'is_submitted': 0,
        'is_late': 0,
        'is_active': 1,
        'created_at': now_iso
    }
    record = SubmissionRecord.from_row(row)
    assert record.id == 1
    assert record.is_submitted is False
    assert record.created_at.isoformat() == now_iso
