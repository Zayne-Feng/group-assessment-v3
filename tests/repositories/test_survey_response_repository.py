import pytest
from app.repositories.survey_response_repository import survey_response_repository
from app.models.survey_response import SurveyResponse
from app.repositories.student_repository import student_repository
from app.repositories.module_repository import module_repository

# --- Fixtures ---
@pytest.fixture(scope="module")
def sample_student():
    return student_repository.create_student('S_SURVEY_TEST', 'Survey Test Student', 'survey.test@example.com', 'MSc Survey Testing', 1)

@pytest.fixture(scope="module")
def sample_module():
    return module_repository.create_module('SURVEY101', 'Survey Testing', 15, '2025')

# --- Integration Test ---
def test_create_and_get_survey_response(sample_student, sample_module):
    new_response = survey_response_repository.create_survey_response(student_id=sample_student.id, module_id=sample_module.id, week_number=4, stress_level=5, hours_slept=6.5, mood_comment="Feeling stressed")
    assert new_response is not None
    fetched_response = survey_response_repository.get_survey_response_by_id(new_response.id)
    assert fetched_response.stress_level == 5

# --- Unit Tests for Business Logic ---
def test_check_for_stress_event_creation(mocker):
    mock_db = mocker.patch('app.repositories.survey_response_repository.get_db')
    mock_cursor = mock_db.return_value.execute
    mock_cursor.return_value.fetchone.return_value = None
    high_stress_survey = SurveyResponse(id=1, student_id=1, module_id=1, week_number=5, stress_level=5)
    survey_response_repository._check_for_stress_events_and_alerts(high_stress_survey, threshold=4)
    insert_call_args = mock_cursor.call_args_list[1][0][0]
    assert "INSERT INTO stress_events" in insert_call_args
    assert mock_db.return_value.commit.call_count == 1

def test_check_for_alert_creation(mocker):
    mock_db = mocker.patch('app.repositories.survey_response_repository.get_db')
    mock_cursor = mock_db.return_value.execute
    mock_cursor.return_value.fetchone.side_effect = [
        None,
        {'week_number': 4, 'stress_level': 4},
        None
    ]
    current_high_stress_survey = SurveyResponse(id=2, student_id=1, module_id=1, week_number=5, stress_level=4)
    survey_response_repository._check_for_stress_events_and_alerts(current_high_stress_survey, threshold=4)
    # The call order is: SELECT stress_event, INSERT stress_event, SELECT previous_survey, SELECT alert, INSERT alert
    assert "INSERT INTO alerts" in mock_cursor.call_args_list[4][0][0]
    assert mock_db.return_value.commit.call_count == 2

def test_no_event_or_alert_on_low_stress(mocker):
    mock_db = mocker.patch('app.repositories.survey_response_repository.get_db')
    mock_execute = mock_db.return_value.execute
    # Simulate finding a low-stress survey from the previous week
    mock_execute.return_value.fetchone.return_value = {'week_number': 5, 'stress_level': 2}
    
    low_stress_survey = SurveyResponse(id=3, student_id=1, module_id=1, week_number=6, stress_level=3)
    survey_response_repository._check_for_stress_events_and_alerts(low_stress_survey, threshold=4)
    
    for call in mock_execute.call_args_list:
        assert "INSERT" not in call[0][0]
    assert mock_db.return_value.commit.call_count == 0
