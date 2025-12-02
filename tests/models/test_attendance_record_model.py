import pytest
from app.models.attendance_record import AttendanceRecord
from datetime import datetime

def test_attendance_record_initialization():
    """Tests the initialization of the AttendanceRecord model."""
    record = AttendanceRecord(id=1, student_id=2, module_id=3, week_number=5, attended_sessions=2, total_sessions=2)
    assert record.id == 1
    assert record.week_number == 5
    assert record.attended_sessions == 2

def test_attendance_record_to_dict():
    """Tests the to_dict method of the AttendanceRecord model."""
    now = datetime.now()
    record = AttendanceRecord(id=1, student_id=2, created_at=now)
    record_dict = record.to_dict()
    assert record_dict['id'] == 1
    assert record_dict['student_id'] == 2
    assert record_dict['created_at'] == now.isoformat()

def test_attendance_record_from_row():
    """Tests the from_row class method of the AttendanceRecord model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'week_number': 5,
        'attended_sessions': 2,
        'total_sessions': 2,
        'attendance_rate': 1.0,
        'is_active': 1,
        'created_at': now_iso
    }
    record = AttendanceRecord.from_row(row)
    assert record.id == 1
    assert record.attendance_rate == 1.0
    assert record.created_at.isoformat() == now_iso
