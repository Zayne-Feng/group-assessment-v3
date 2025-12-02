"""
Alert Repository module for managing alert-related data.

This module defines the `AlertRepository` class, which provides methods
for interacting with the 'alerts' table in the database. It extends
`BaseRepository` to handle CRUD operations for alerts, including
retrieving specific alerts, marking them as resolved, and creating new ones.
"""

import sqlite3
from app.db_connection import get_db
from app.models.alert import Alert
from .base_repository import BaseRepository

class AlertRepository(BaseRepository):
    """
    Repository for alert-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student alerts, often joining with student and module information.
    """
    def __init__(self):
        """
        Initializes the AlertRepository.

        Sets the table name to 'alerts' and the model class to `Alert`.
        """
        super().__init__('alerts', Alert)

    def get_all_alerts(self) -> list[dict]:
        """
        Retrieves all active alerts from the database, including associated
        student and module information for richer context.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents
                        an alert with joined student and module details.
        """
        query = """
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            WHERE a.is_active = 1
            ORDER BY a.created_at DESC
        """
        # _execute_query handles exceptions and returns results as dictionaries due to fetch_all_dicts=True.
        return self._execute_query(query, fetch_all_dicts=True)

    def get_recent_alerts_per_student(self) -> list[dict]:
        """
        Retrieves the most recent active alert for each student.

        This query identifies the latest alert (by week number) for every student
        and fetches its details along with student and module information.

        Returns:
            list[dict]: A list of dictionaries, each representing the latest
                        active alert for a distinct student.
        """
        query = """
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            JOIN (
                SELECT student_id, MAX(week_number) AS max_week_number
                FROM alerts
                WHERE is_active = 1
                GROUP BY student_id
            ) AS latest_alerts
            ON a.student_id = latest_alerts.student_id AND a.week_number = latest_alerts.max_week_number
            WHERE a.is_active = 1
            ORDER BY a.week_number DESC, a.created_at DESC
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_alerts_by_student_id(self, student_id: int) -> list[dict]:
        """
        Retrieves all active alerts for a specific student.

        Args:
            student_id (int): The unique identifier of the student.

        Returns:
            list[dict]: A list of dictionaries, each representing an active alert
                        associated with the given student, including joined details.
        """
        query = """
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            WHERE a.student_id = ? AND a.is_active = 1
            ORDER BY a.created_at DESC
        """
        return self._execute_query(query, (student_id,), fetch_all_dicts=True)

    def get_alert_by_id(self, alert_id: int) -> Alert | None:
        """
        Retrieves a single alert by its unique ID.

        Args:
            alert_id (int): The unique identifier of the alert to retrieve.

        Returns:
            Alert | None: An `Alert` object if found, otherwise None.
        """
        return super().get_by_id(alert_id)

    def mark_alert_resolved(self, alert_id: int) -> bool:
        """
        Marks a specific alert as resolved in the database.

        Args:
            alert_id (int): The unique identifier of the alert to mark as resolved.

        Returns:
            bool: True if the alert was successfully marked as resolved (i.e., a record was updated), False otherwise.
        """
        query = "UPDATE alerts SET resolved = 1 WHERE id = ?"
        return self._execute_update_delete(query, (alert_id,))
    
    def delete_alert(self, alert_id: int) -> bool:
        """
        Logically deletes an alert by setting its 'is_active' flag to 0.

        Args:
            alert_id (int): The unique identifier of the alert to logically delete.

        Returns:
            bool: True if the alert was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(alert_id)

    def create_alert(self, student_id: int, module_id: int | None, week_number: int, reason: str) -> Alert:
        """
        Creates a new alert record in the database.

        Args:
            student_id (int): The ID of the student to whom the alert pertains.
            module_id (int | None): The ID of the module related to the alert (can be None).
            week_number (int): The week number when the alert was generated.
            reason (str): The descriptive reason for the alert.

        Returns:
            Alert: The newly created `Alert` object.
        """
        query = "INSERT INTO alerts (student_id, module_id, week_number, reason, resolved, is_active) VALUES (?, ?, ?, ?, 0, 1)"
        alert_id = self._execute_insert(query, (student_id, module_id, week_number, reason))
        return self.get_alert_by_id(alert_id)

# Instantiate the repository for use throughout the application.
alert_repository = AlertRepository()
