import sqlite3
from app.db_connection import get_db
from app.models.survey_response import SurveyResponse
from app.models.stress_event import StressEvent
from app.models.alert import Alert
from datetime import datetime
from .base_repository import BaseRepository

class SurveyResponseRepository(BaseRepository):
    def __init__(self):
        super().__init__('survey_responses', SurveyResponse)

    def get_all_survey_responses(self):
        query = """
            SELECT 
                sr.id, sr.student_id, sr.module_id, sr.week_number, 
                sr.stress_level, sr.hours_slept, sr.mood_comment, sr.created_at,
                s.full_name as student_name,
                m.module_title as module_title
            FROM survey_responses sr
            LEFT JOIN students s ON sr.student_id = s.id
            LEFT JOIN modules m ON sr.module_id = m.id
            WHERE sr.is_active = 1
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_survey_response_by_id(self, response_id):
        return super().get_by_id(response_id)

    def create_survey_response(self, student_id, module_id, week_number, stress_level, hours_slept, mood_comment):
        created_at = datetime.utcnow().isoformat()
        query = """
            INSERT INTO survey_responses (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """
        response_id = self._execute_insert(query, (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at))
        new_survey = self.get_survey_response_by_id(response_id)
        if new_survey:
            self._check_for_stress_events_and_alerts(new_survey)
        return new_survey

    def update_survey_response(self, response_id, student_id, module_id, week_number, stress_level, hours_slept, mood_comment):
        query = """
            UPDATE survey_responses SET student_id = ?, module_id = ?, week_number = ?, stress_level = ?, hours_slept = ?, mood_comment = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, response_id))
        updated_survey = self.get_survey_response_by_id(response_id)
        if updated_survey:
            self._check_for_stress_events_and_alerts(updated_survey)
        return updated_survey

    def delete_survey_response(self, response_id):
        return super().delete_logical(response_id)

    def _check_for_stress_events_and_alerts(self, survey_response: SurveyResponse, threshold: int = 4):
        db = get_db()
        try:
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
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error in _check_for_stress_events_and_alerts: {e}")
            raise Exception("Error checking for stress events and alerts.")

# Instantiate the repository for use
survey_response_repository = SurveyResponseRepository()
