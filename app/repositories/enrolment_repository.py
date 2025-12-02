"""
Enrolment Repository module for managing student enrolment data.

This module defines the `EnrolmentRepository` class, which provides methods
for interacting with the 'enrolments' table in the database. It extends
`BaseRepository` to handle CRUD operations for enrolments, including
retrieving records with joined student and module information.
"""

import sqlite3
from app.db_connection import get_db
from app.models.enrolment import Enrolment
from datetime import datetime, timezone
from .base_repository import BaseRepository

class EnrolmentRepository(BaseRepository):
    """
    Repository for enrolment-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student enrolments.
    """
    def __init__(self):
        """
        Initializes the EnrolmentRepository.

        Sets the table name to 'enrolments' and the model class to `Enrolment`.
        """
        super().__init__('enrolments', Enrolment)

    def get_all_enrolments(self) -> list[dict]:
        """
        Retrieves all active enrolments from the database, including associated
        student and module information for richer context.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents
                        an enrolment with joined student and module details.
        """
        query = """
            SELECT e.id, e.student_id, e.module_id, e.enrol_date, e.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM enrolments e
            JOIN students s ON e.student_id = s.id
            JOIN modules m ON e.module_id = m.id
            WHERE e.is_active = 1
        """
        # _execute_query handles exceptions and returns results as dictionaries due to fetch_all_dicts=True.
        return self._execute_query(query, fetch_all_dicts=True)

    def get_enrolment_by_id(self, enrolment_id: int) -> Enrolment | None:
        """
        Retrieves a single enrolment by its unique ID.

        Args:
            enrolment_id (int): The unique identifier of the enrolment to retrieve.

        Returns:
            Enrolment | None: An `Enrolment` object if found, otherwise None.
        """
        return super().get_by_id(enrolment_id)

    def create_enrolment(self, student_id: int, module_id: int, enrol_date: str | None = None) -> Enrolment:
        """
        Creates a new enrolment record in the database.

        Args:
            student_id (int): The ID of the student to enroll.
            module_id (int): The ID of the module to enroll in.
            enrol_date (str, optional): The enrolment date in ISO format. Defaults to the current UTC date.

        Returns:
            Enrolment: The newly created `Enrolment` object.
        """
        # Default enrol_date to current UTC date if not provided.
        if enrol_date is None:
            enrol_date = datetime.now(timezone.utc).date().isoformat()
        query = "INSERT INTO enrolments (student_id, module_id, enrol_date, is_active) VALUES (?, ?, ?, 1)"
        enrolment_id = self._execute_insert(query, (student_id, module_id, enrol_date))
        return self.get_enrolment_by_id(enrolment_id)

    def update_enrolment(self, enrolment_id: int, student_id: int, module_id: int, enrol_date: str) -> Enrolment:
        """
        Updates an existing enrolment record in the database.

        Args:
            enrolment_id (int): The unique identifier of the enrolment to update.
            student_id (int): The new student ID for the enrolment.
            module_id (int): The new module ID for the enrolment.
            enrol_date (str): The new enrolment date in ISO format.

        Returns:
            Enrolment: The updated `Enrolment` object.
        """
        query = "UPDATE enrolments SET student_id = ?, module_id = ?, enrol_date = ? WHERE id = ?"
        self._execute_update_delete(query, (student_id, module_id, enrol_date, enrolment_id))
        return self.get_enrolment_by_id(enrolment_id)

    def delete_enrolment(self, enrolment_id: int) -> bool:
        """
        Logically deletes an enrolment by setting its 'is_active' flag to 0.

        Args:
            enrolment_id (int): The unique identifier of the enrolment to logically delete.

        Returns:
            bool: True if the enrolment was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(enrolment_id)

# Instantiate the repository for use throughout the application.
enrolment_repository = EnrolmentRepository()
