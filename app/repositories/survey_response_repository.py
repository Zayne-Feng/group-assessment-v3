"""
Survey Response Repository module for managing student survey data.

This module defines the `SurveyResponseRepository` class, which provides methods
for interacting with the 'survey_responses' table in the database. It extends
`BaseRepository` to handle CRUD operations for survey responses and includes
logic to automatically check for and create stress events and alerts based
on the submitted survey data.
"""

import sqlite3
from app.db_connection import get_db
from app.models.survey_response import SurveyResponse
from app.models.stress_event import StressEvent # Imported for type hinting/context
from app.models.alert import Alert # Imported for type hinting/context
from datetime import datetime, timezone
from .base_repository import BaseRepository
from flask import current_app # Import current_app for logging

class SurveyResponseRepository(BaseRepository):
    """
    Repository for survey response-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student survey responses, and integrates logic for automatic stress
    event and alert generation.
    """
    def __init__(self):
        """
        Initializes the SurveyResponseRepository.

        Sets the table name to 'survey_responses' and the model class to `SurveyResponse`.
        """
        super().__init__('survey_responses', SurveyResponse)

    def get_all_survey_responses(self) -> list[dict]:
        """
        Retrieves all active survey responses from the database, including
        associated student and module information for richer context.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents
                        a survey response with joined student and module details.
        """
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
        # _execute_query handles exceptions and returns results as dictionaries due to fetch_all_dicts=True.
        return self._execute_query(query, fetch_all_dicts=True)

    def get_survey_response_by_id(self, response_id: int) -> SurveyResponse | None:
        """
        Retrieves a single survey response by its unique ID.

        Args:
            response_id (int): The unique identifier of the survey response to retrieve.

        Returns:
            SurveyResponse | None: A `SurveyResponse` object if found, otherwise None.
        """
        return super().get_by_id(response_id)

    def create_survey_response(self, student_id: int, module_id: int | None, week_number: int, stress_level: int, hours_slept: float, mood_comment: str | None) -> SurveyResponse:
        """
        Creates a new survey response in the database.

        After creation, it automatically triggers a check for stress events and alerts
        based on the new response's stress level.

        Args:
            student_id (int): The ID of the student submitting the response.
            module_id (int | None): The ID of the module related to the survey (can be None).
            week_number (int): The academic week number of the survey.
            stress_level (int): The reported stress level (e.g., 1-5).
            hours_slept (float): The reported hours of sleep.
            mood_comment (str | None): Any comments on the mood.

        Returns:
            SurveyResponse: The newly created `SurveyResponse` object.
        """
        created_at = datetime.now(timezone.utc).isoformat()
        query = """
            INSERT INTO survey_responses (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """
        response_id = self._execute_insert(query, (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at))
        new_survey = self.get_survey_response_by_id(response_id)
        if new_survey:
            # Trigger the check for stress events and alerts.
            self._check_for_stress_events_and_alerts(new_survey)
        return new_survey

    def update_survey_response(self, response_id: int, student_id: int, module_id: int | None, week_number: int, stress_level: int, hours_slept: float, mood_comment: str | None) -> SurveyResponse:
        """
        Updates an existing survey response in the database.

        After updating, it re-triggers a check for stress events and alerts
        based on the modified response's stress level.

        Args:
            response_id (int): The unique identifier of the survey response to update.
            student_id (int): The new student ID for the response.
            module_id (int | None): The new module ID for the response.
            week_number (int): The new week number for the response.
            stress_level (int): The new reported stress level.
            hours_slept (float): The new reported hours of sleep.
            mood_comment (str | None): The new mood comment.

        Returns:
            SurveyResponse: The updated `SurveyResponse` object.
        """
        query = """
            UPDATE survey_responses SET student_id = ?, module_id = ?, week_number = ?, stress_level = ?, hours_slept = ?, mood_comment = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, response_id))
        updated_survey = self.get_survey_response_by_id(response_id)
        if updated_survey:
            # Trigger the check for stress events and alerts after update.
            self._check_for_stress_events_and_alerts(updated_survey)
        return updated_survey

    def delete_survey_response(self, response_id: int) -> bool:
        """
        Logically deletes a survey response by setting its 'is_active' flag to 0.

        Args:
            response_id (int): The unique identifier of the survey response to logically delete.

        Returns:
            bool: True if the survey response was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(response_id)

    def _check_for_stress_events_and_alerts(self, survey_response: SurveyResponse, threshold: int = 4):
        """
        Private method to check for and create stress events and alerts based on a survey response.

        This method is called internally after a survey response is created or updated.
        It performs two main checks:
        1. If the current stress level is above a threshold, it creates a `StressEvent`.
        2. If the student has reported high stress for two consecutive weeks, it creates an `Alert`.

        Args:
            survey_response (SurveyResponse): The survey response object to check.
            threshold (int, optional): The stress level threshold (1-5) to trigger events/alerts. Defaults to 4.
        
        Raises:
            Exception: If a database error occurs during the check or creation of events/alerts.
        """
        db = get_db()
        try:
            # 1. Check for StressEvent: If stress level is high, record a stress event.
            if survey_response.stress_level >= threshold:
                # Check if an event for this survey response already exists to prevent duplicates.
                cursor = db.execute("SELECT id FROM stress_events WHERE survey_response_id = ?", (survey_response.id,))
                existing_event = cursor.fetchone()
                if not existing_event:
                    stress_event_created_at = datetime.now(timezone.utc).isoformat()
                    db.execute(
                        "INSERT INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                        (survey_response.student_id, survey_response.module_id, survey_response.id, survey_response.week_number, survey_response.stress_level, "system_detected", f"High stress reported (level {survey_response.stress_level}) in week {survey_response.week_number}.", "survey_response_system", stress_event_created_at)
                    )
                    db.commit()
                    current_app.logger.info(f"Stress event created for student {survey_response.student_id} (level {survey_response.stress_level}).")

            # 2. Check for Alerts: Identify consecutive high stress levels.
            # Retrieve the survey response from the previous week for the same student and module.
            cursor = db.execute("""
                SELECT week_number, stress_level FROM survey_responses
                WHERE student_id = ? AND module_id = ? AND week_number = ? AND is_active = 1
            """, (survey_response.student_id, survey_response.module_id, survey_response.week_number - 1))
            previous_week_survey_row = cursor.fetchone()

            # If both current and previous week's stress levels are above the threshold, create an alert.
            if previous_week_survey_row and \
               previous_week_survey_row['stress_level'] >= threshold and \
               survey_response.stress_level >= threshold:
                
                # Check if an alert for this specific week already exists to prevent duplicates.
                cursor = db.execute("SELECT id FROM alerts WHERE student_id = ? AND week_number = ? AND is_active = 1", (survey_response.student_id, survey_response.week_number))
                existing_alert = cursor.fetchone()

                if not existing_alert:
                    alert_created_at = datetime.now(timezone.utc).isoformat()
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
                    current_app.logger.warning(f"Alert created for student {survey_response.student_id}: Consecutive high stress detected.")
        except sqlite3.Error as e:
            db.rollback() # Rollback changes if any database error occurs during this process.
            current_app.logger.error(f"Database error in _check_for_stress_events_and_alerts: {e}", exc_info=True)
            raise Exception("Error checking for stress events and alerts.") # Re-raise for higher-level handling.

# Instantiate the repository for use throughout the application.
survey_response_repository = SurveyResponseRepository()
