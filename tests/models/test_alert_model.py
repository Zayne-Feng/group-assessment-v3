import pytest
from app.models.alert import Alert
from datetime import datetime

def test_alert_initialization():
    """Tests the initialization of the Alert model."""
    alert = Alert(id=1, student_id=2, module_id=3, week_number=4, reason="Test", resolved=True)
    assert alert.id == 1
    assert alert.student_id == 2
    assert alert.reason == "Test"
    assert alert.resolved is True

def test_alert_to_dict():
    """Tests the to_dict method of the Alert model."""
    now = datetime.now()
    alert = Alert(id=1, student_id=2, created_at=now)
    alert_dict = alert.to_dict()
    assert alert_dict['id'] == 1
    assert alert_dict['student_id'] == 2
    assert alert_dict['created_at'] == now.isoformat()

def test_alert_from_row():
    """Tests the from_row class method of the Alert model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'week_number': 4,
        'reason': 'Test',
        'resolved': 1,
        'is_active': 1,
        'created_at': now_iso
    }
    alert = Alert.from_row(row)
    assert alert.id == 1
    assert alert.student_id == 2
    assert alert.resolved is True
    assert alert.created_at.isoformat() == now_iso
