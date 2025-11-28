from app.db_connection import get_db
from app.models.survey_response import SurveyResponse
from app.models.stress_event import StressEvent
from app.models.alert import Alert
from datetime import datetime

class SurveyResponseRepository:
    @staticmethod
    def get_all_survey_responses():
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active FROM survey_responses WHERE is_active = 1")
        surveys = [SurveyResponse.from_row(row) for row in cursor.fetchall()]
        return surveys

    @staticmethod
    def get_survey_response_by_id(response_id):
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active FROM survey_responses WHERE id = ? AND is_active = 1", (response_id,))
        survey = SurveyResponse.from_row(cursor.fetchone())
        return survey

    @staticmethod
    def create_survey_response(student_id, module_id, week_number, stress_level, hours_slept, mood_comment):
        db = get_db()
        created_at = datetime.utcnow().isoformat()
        
        cursor = db.execute(
            "INSERT INTO survey_responses (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
            (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at)
        )
        db.commit()
        new_survey = SurveyResponse(id=cursor.lastrowid, student_id=student_id, module_id=module_id, week_number=week_number, stress_level=stress_level, hours_slept=hours_slept, mood_comment=mood_comment, created_at=created_at)
        
        # After creating survey, check for stress events and alerts
        SurveyResponseRepository._check_for_stress_events_and_alerts(new_survey)
        
        return new_survey

    @staticmethod
    def update_survey_response(response_id, student_id, module_id, week_number, stress_level, hours_slept, mood_comment):
        db = get_db()
        db.execute(
            "UPDATE survey_responses SET student_id = ?, module_id = ?, week_number = ?, stress_level = ?, hours_slept = ?, mood_comment = ? WHERE id = ?",
            (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, response_id)
        )
        db.commit()
        updated_survey = SurveyResponseRepository.get_survey_response_by_id(response_id)
        if updated_survey:
            SurveyResponseRepository._check_for_stress_events_and_alerts(updated_survey)
        return updated_survey

    @staticmethod
    def delete_survey_response(response_id):
        db = get_db()
        db.execute("UPDATE survey_responses SET is_active = 0 WHERE id = ?", (response_id,))
        db.commit()
        return True

    @staticmethod
    def _check_for_stress_events_and_alerts(survey_response: SurveyResponse, threshold: int = 4):
        """
        Internal method to check for stress events and alerts based on a new/updated survey response.
        """
        db = get_db()
        
        # 1. Check for StressEvent
        if survey_response.stress_level >= threshold:
            cursor = db.execute("SELECT id FROM stress_events WHERE survey_response_id = ?", (survey_response.id,))
            existing_event = cursor.fetchone()
            if not existing_event:
                stress_event_created_at = datetime.utcnow().isoformat()
                db.execute(
                    "INSERT INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (survey_response.student_id, survey_response.module_id, survey_response.id, survey_response.week_number, survey_response.stress_level, "system_detected", f"High stress reported (level {survey_response.stress_level}) in week {survey_response.week_number}.", "survey_response_system", stress_event_created_at)
                )
                db.commit()

        # 2. Check for Alerts (consecutive high stress)
        cursor = db.execute("""
            SELECT week_number, stress_level FROM survey_responses
            WHERE student_id = ? AND module_id = ? AND week_number = ? AND is_active = 1
        """, (survey_response.student_id, survey_response.module_id, survey_response.week_number - 1))
        previous_week_survey_row = cursor.fetchone()

        if previous_week_survey_row and \
           previous_week_survey_row['stress_level'] >= threshold and \
           survey_response.stress_level >= threshold:
            
            cursor = db.execute("SELECT id FROM alerts WHERE student_id = ? AND week_number = ? AND is_active = 1", (survey_response.student_id, survey_response.week_number))
            existing_alert = cursor.fetchone()

            if not existing_alert:
                alert_created_at = datetime.utcnow().isoformat()
                alert_reason = (
                    f"Stress level >= {threshold} for two consecutive weeks "
                    f"({survey_response.week_number - 1} and {survey_response.week_number}) "
                    f"for student {survey_response.student_id} in module {survey_response.module_id}."
                )
                db.execute(
                    "INSERT INTO alerts (student_id, module_id, week_number, reason, created_at, resolved, is_active) VALUES (?, ?, ?, ?, ?, 0, 1)",
                    (survey_response.student_id, survey_response.module_id, survey_response.week_number, alert_reason, alert_created_at)
                )
                db.commit()
