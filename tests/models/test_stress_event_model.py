import pytest
from app.models.stress_event import StressEvent
from datetime import datetime

def test_stress_event_initialization():
    """Tests the initialization of the StressEvent model."""
    event = StressEvent(id=1, student_id=2, module_id=3, week_number=7, stress_level=5, cause_category='academic')
    assert event.id == 1
    assert event.week_number == 7
    assert event.cause_category == 'academic'

def test_stress_event_to_dict():
    """Tests the to_dict method of the StressEvent model."""
    now = datetime.now()
    event = StressEvent(id=1, student_id=2, created_at=now)
    event_dict = event.to_dict()
    assert event_dict['id'] == 1
    assert event_dict['student_id'] == 2
    assert event_dict['created_at'] == now.isoformat()

def test_stress_event_from_row():
    """Tests the from_row class method of the StressEvent model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'survey_response_id': 4,
        'week_number': 7,
        'stress_level': 5,
        'cause_category': 'academic',
        'description': 'Exam pressure',
        'source': 'manual',
        'is_active': 1,
        'created_at': now_iso
    }
    event = StressEvent.from_row(row)
    assert event.id == 1
    assert event.stress_level == 5
    assert event.created_at.isoformat() == now_iso
