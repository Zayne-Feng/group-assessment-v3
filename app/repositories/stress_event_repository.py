"""
Stress Event Repository module for managing student stress event data.

This module defines the `StressEventRepository` class, which provides methods
for interacting with the 'stress_events' table in the database. It extends
`BaseRepository` to handle CRUD operations for stress events, including
retrieving, creating, updating, and logically deleting event records.
"""

import sqlite3
from app.db_connection import get_db
from app.models.stress_event import StressEvent
from datetime import datetime, timezone
from .base_repository import BaseRepository

class StressEventRepository(BaseRepository):
    """
    Repository for stress event-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    records of student stress events.
    """
    def __init__(self):
        """
        Initializes the StressEventRepository.

        Sets the table name to 'stress_events' and the model class to `StressEvent`.
        """
        super().__init__('stress_events', StressEvent)

    def get_all_stress_events(self) -> list[StressEvent]:
        """
        Retrieves all active stress events from the database.

        Returns:
            list[StressEvent]: A list of `StressEvent` objects representing all active events.
        """
        return super().get_all()

    def get_stress_event_by_id(self, event_id: int) -> StressEvent | None:
        """
        Retrieves a single stress event by its unique ID.

        Args:
            event_id (int): The unique identifier of the stress event to retrieve.

        Returns:
            StressEvent | None: A `StressEvent` object if found, otherwise None.
        """
        return super().get_by_id(event_id)

    def create_stress_event(self, student_id: int, module_id: int | None, survey_response_id: int | None, week_number: int, stress_level: int, cause_category: str, description: str | None, source: str) -> StressEvent:
        """
        Creates a new stress event record in the database.

        Args:
            student_id (int): The ID of the student experiencing the event.
            module_id (int | None): The ID of the module related to the event (can be None).
            survey_response_id (int | None): The ID of the associated survey response (can be None).
            week_number (int): The academic week number when the event occurred.
            stress_level (int): The reported or detected stress level (e.g., 1-5).
            cause_category (str): The category of the cause (e.g., 'academic', 'personal').
            description (str | None): A detailed description of the stress event.
            source (str): The source that identified the stress event (e.g., 'system', 'survey').

        Returns:
            StressEvent: The newly created `StressEvent` object.
        """
        created_at = datetime.now(timezone.utc).isoformat() # Set creation timestamp.
        query = """
            INSERT INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """
        event_id = self._execute_insert(query, (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at))
        return self.get_stress_event_by_id(event_id)

    def update_stress_event(self, event_id: int, student_id: int, module_id: int | None, survey_response_id: int | None, week_number: int, stress_level: int, cause_category: str, description: str | None, source: str) -> StressEvent:
        """
        Updates an existing stress event record in the database.

        Args:
            event_id (int): The unique identifier of the stress event to update.
            student_id (int): The new student ID for the event.
            module_id (int | None): The new module ID for the event.
            survey_response_id (int | None): The new survey response ID for the event.
            week_number (int): The new week number for the event.
            stress_level (int): The new stress level for the event.
            cause_category (str): The new cause category for the event.
            description (str | None): The new description for the event.
            source (str): The new source for the event.

        Returns:
            StressEvent: The updated `StressEvent` object.
        """
        query = """
            UPDATE stress_events SET student_id = ?, module_id = ?, survey_response_id = ?, week_number = ?, stress_level = ?, cause_category = ?, description = ?, source = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, event_id))
        return self.get_stress_event_by_id(event_id)

    def delete_stress_event(self, event_id: int) -> bool:
        """
        Logically deletes a stress event by setting its 'is_active' flag to 0.

        Args:
            event_id (int): The unique identifier of the stress event to logically delete.

        Returns:
            bool: True if the event was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(event_id)

# Instantiate the repository for use throughout the application.
stress_event_repository = StressEventRepository()
