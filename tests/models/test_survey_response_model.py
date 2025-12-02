import pytest
from app.models.survey_response import SurveyResponse
from datetime import datetime

def test_survey_response_initialization():
    """Tests the initialization of the SurveyResponse model."""
    response = SurveyResponse(id=1, student_id=2, module_id=3, week_number=6, stress_level=5)
    assert response.id == 1
    assert response.week_number == 6
    assert response.stress_level == 5

def test_survey_response_to_dict():
    """Tests the to_dict method of the SurveyResponse model."""
    now = datetime.now()
    response = SurveyResponse(id=1, student_id=2, created_at=now)
    response_dict = response.to_dict()
    assert response_dict['id'] == 1
    assert response_dict['student_id'] == 2
    assert response_dict['created_at'] == now.isoformat()

def test_survey_response_from_row():
    """Tests the from_row class method of the SurveyResponse model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'student_id': 2,
        'module_id': 3,
        'week_number': 6,
        'stress_level': 5,
        'hours_slept': 7.5,
        'mood_comment': 'OK',
        'is_active': 1,
        'created_at': now_iso
    }
    response = SurveyResponse.from_row(row)
    assert response.id == 1
    assert response.stress_level == 5
    assert response.created_at.isoformat() == now_iso
