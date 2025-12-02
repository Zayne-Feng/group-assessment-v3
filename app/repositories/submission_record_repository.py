"""
Submission Record Repository module for managing student assessment submission data.

This module defines the `SubmissionRecordRepository` class, which provides methods
for interacting with the 'submission_records' table in the database. It extends
`BaseRepository` to handle CRUD operations for submission records, including
retrieving records with joined student and module information.
"""

import sqlite3
from app.db_connection import get_db
from app.models.submission_record import SubmissionRecord
from .base_repository import BaseRepository

class SubmissionRecordRepository(BaseRepository):
    """
    Repository for submission record-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student assessment submission records.
    """
    def __init__(self):
        """
        Initializes the SubmissionRecordRepository.

        Sets the table name to 'submission_records' and the model class to `SubmissionRecord`.
        """
        super().__init__('submission_records', SubmissionRecord)

    def get_all_submission_records(self) -> list[dict]:
        """
        Retrieves all active submission records from the database, including
        associated student and module information for richer context.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents
                        a submission record with joined student and module details.
        """
        query = """
            SELECT sr.id, sr.student_id, sr.module_id, sr.assessment_name, sr.due_date, sr.submitted_date, sr.is_submitted, sr.is_late, sr.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM submission_records sr
            JOIN students s ON sr.student_id = s.id
            JOIN modules m ON sr.module_id = m.id
            WHERE sr.is_active = 1
        """
        # _execute_query handles exceptions and returns results as dictionaries due to fetch_all_dicts=True.
        return self._execute_query(query, fetch_all_dicts=True)

    def get_submission_record_by_id(self, record_id: int) -> SubmissionRecord | None:
        """
        Retrieves a single submission record by its unique ID.

        Args:
            record_id (int): The unique identifier of the submission record to retrieve.

        Returns:
            SubmissionRecord | None: A `SubmissionRecord` object if found, otherwise None.
        """
        return super().get_by_id(record_id)

    def create_submission_record(self, student_id: int, module_id: int, assessment_name: str, due_date: str, submitted_date: str | None, is_submitted: bool, is_late: bool) -> SubmissionRecord:
        """
        Creates a new submission record in the database.

        Args:
            student_id (int): The ID of the student who made the submission.
            module_id (int): The ID of the module to which the assessment belongs.
            assessment_name (str): The name of the assessment.
            due_date (str): The due date of the assessment in ISO format.
            submitted_date (str | None): The actual submission date in ISO format, or None if not submitted.
            is_submitted (bool): True if the assessment was submitted, False otherwise.
            is_late (bool): True if the submission was late, False otherwise.

        Returns:
            SubmissionRecord: The newly created `SubmissionRecord` object.
        """
        query = """
            INSERT INTO submission_records (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """
        record_id = self._execute_insert(query, (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late))
        return self.get_submission_record_by_id(record_id)

    def update_submission_record(self, record_id: int, student_id: int, module_id: int, assessment_name: str, due_date: str, submitted_date: str | None, is_submitted: bool, is_late: bool) -> SubmissionRecord:
        """
        Updates an existing submission record in the database.

        Args:
            record_id (int): The unique identifier of the record to update.
            student_id (int): The new student ID for the record.
            module_id (int): The new module ID for the record.
            assessment_name (str): The new assessment name.
            due_date (str): The new due date in ISO format.
            submitted_date (str | None): The new submission date in ISO format, or None.
            is_submitted (bool): The new submission status.
            is_late (bool): The new late status.

        Returns:
            SubmissionRecord: The updated `SubmissionRecord` object.
        """
        query = """
            UPDATE submission_records SET student_id = ?, module_id = ?, assessment_name = ?, due_date = ?, submitted_date = ?, is_submitted = ?, is_late = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, record_id))
        return self.get_submission_record_by_id(record_id)

    def delete_submission_record(self, record_id: int) -> bool:
        """
        Logically deletes a submission record by setting its 'is_active' flag to 0.

        Args:
            record_id (int): The unique identifier of the submission record to logically delete.

        Returns:
            bool: True if the record was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(record_id)

# Instantiate the repository for use throughout the application.
submission_record_repository = SubmissionRecordRepository()
