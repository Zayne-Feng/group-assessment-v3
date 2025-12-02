"""
Attendance Record Repository module for managing student attendance data.

This module defines the `AttendanceRecordRepository` class, which provides
methods for interacting with the 'attendance_records' table in the database.
It extends `BaseRepository` to handle CRUD operations for attendance records,
including calculating attendance rates and retrieving records with joined
student and module information.
"""

import sqlite3
from app.db_connection import get_db
from app.models.attendance_record import AttendanceRecord
from .base_repository import BaseRepository

class AttendanceRecordRepository(BaseRepository):
    """
    Repository for attendance record-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student attendance records, including calculated attendance rates.
    """
    def __init__(self):
        """
        Initializes the AttendanceRecordRepository.

        Sets the table name to 'attendance_records' and the model class to `AttendanceRecord`.
        """
        super().__init__('attendance_records', AttendanceRecord)

    def get_all_attendance_records(self) -> list[dict]:
        """
        Retrieves all active attendance records from the database, including
        associated student and module information for richer context.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents
                        an attendance record with joined student and module details.
        """
        query = """
            SELECT ar.id, ar.student_id, ar.module_id, ar.week_number, ar.attended_sessions, ar.total_sessions, ar.attendance_rate, ar.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM attendance_records ar
            JOIN students s ON ar.student_id = s.id
            JOIN modules m ON ar.module_id = m.id
            WHERE ar.is_active = 1
        """
        # _execute_query handles exceptions and returns results as dictionaries due to fetch_all_dicts=True.
        return self._execute_query(query, fetch_all_dicts=True)

    def get_attendance_record_by_id(self, record_id: int) -> AttendanceRecord | None:
        """
        Retrieves a single attendance record by its unique ID.

        Args:
            record_id (int): The unique identifier of the attendance record to retrieve.

        Returns:
            AttendanceRecord | None: An `AttendanceRecord` object if found, otherwise None.
        """
        return super().get_by_id(record_id)

    def create_attendance_record(self, student_id: int, module_id: int, week_number: int, attended_sessions: int, total_sessions: int) -> AttendanceRecord:
        """
        Creates a new attendance record in the database.

        Automatically calculates the `attendance_rate` based on provided sessions.

        Args:
            student_id (int): The ID of the student.
            module_id (int): The ID of the module.
            week_number (int): The academic week number for this record.
            attended_sessions (int): The number of sessions attended by the student.
            total_sessions (int): The total number of sessions held for the module in that week.

        Returns:
            AttendanceRecord: The newly created `AttendanceRecord` object.
        """
        # Calculate attendance rate, handling division by zero.
        attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0.0
        query = """
            INSERT INTO attendance_records (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """
        record_id = self._execute_insert(query, (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate))
        return self.get_attendance_record_by_id(record_id)

    def update_attendance_record(self, record_id: int, student_id: int, module_id: int, week_number: int, attended_sessions: int, total_sessions: int) -> AttendanceRecord:
        """
        Updates an existing attendance record in the database.

        Automatically recalculates the `attendance_rate` based on updated session counts.

        Args:
            record_id (int): The unique identifier of the record to update.
            student_id (int): The new student ID for the record.
            module_id (int): The new module ID for the record.
            week_number (int): The new week number for the record.
            attended_sessions (int): The new number of attended sessions.
            total_sessions (int): The new total number of sessions.

        Returns:
            AttendanceRecord: The updated `AttendanceRecord` object.
        """
        # Recalculate attendance rate based on new values.
        attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0.0
        query = """
            UPDATE attendance_records SET student_id = ?, module_id = ?, week_number = ?, attended_sessions = ?, total_sessions = ?, attendance_rate = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, record_id))
        return self.get_attendance_record_by_id(record_id)

    def delete_attendance_record(self, record_id: int) -> bool:
        """
        Logically deletes an attendance record by setting its 'is_active' flag to 0.

        Args:
            record_id (int): The unique identifier of the attendance record to logically delete.

        Returns:
            bool: True if the record was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(record_id)

# Instantiate the repository for use throughout the application.
attendance_record_repository = AttendanceRecordRepository()
