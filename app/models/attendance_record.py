"""
Attendance Record model definition for the application.

This module defines the `AttendanceRecord` class, representing a student's
attendance status for a specific module during a given week. It inherits
from `BaseModel` for common fields and includes attributes for tracking
attended sessions, total sessions, and calculated attendance rate.
"""

from datetime import datetime
from .base_model import BaseModel

class AttendanceRecord(BaseModel):
    """
    Represents an attendance record for a student in a module for a specific week.

    Inherits from `BaseModel` for common fields such as `id`, `created_at`,
    and `is_active`. Includes attributes to track attendance details and
    optionally related student/module names for display purposes.
    """
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, attended_sessions=None, total_sessions=None, attendance_rate=None, student_name=None, module_title=None, created_at=None, is_active=True, **kwargs):
        """
        Initializes an AttendanceRecord instance.

        Args:
            id (int, optional): The unique identifier for the attendance record.
            student_id (int, optional): The ID of the student associated with this record.
            module_id (int, optional): The ID of the module associated with this record.
            week_number (int, optional): The academic week number this record pertains to.
            attended_sessions (int, optional): The number of sessions the student attended in the week.
            total_sessions (int, optional): The total number of sessions held in the week for the module.
            attendance_rate (float, optional): The calculated attendance rate (attended_sessions / total_sessions).
            student_name (str, optional): The full name of the student (often populated via JOINs).
            module_title (str, optional): The title of the module (often populated via JOINs).
            created_at (datetime, optional): The timestamp when the record was created. Defaults to current UTC time.
            is_active (bool, optional): Whether the record is active. Defaults to True.
            **kwargs: Additional keyword arguments passed to the BaseModel constructor.
        """
        super().__init__(id=id, created_at=created_at, is_active=is_active, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.attended_sessions = attended_sessions
        self.total_sessions = total_sessions
        self.attendance_rate = attendance_rate
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self) -> dict:
        """
        Converts the AttendanceRecord object to a dictionary representation, including common base model fields.

        Returns:
            dict: A dictionary containing the attendance record's attributes suitable for JSON serialization.
        """
        data = super().to_dict() # Get common fields from BaseModel.
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'attended_sessions': self.attended_sessions,
            'total_sessions': self.total_sessions,
            'attendance_rate': self.attendance_rate,
            'student_name': self.student_name,
            'module_title': self.module_title
        })
        return data

    @classmethod
    def from_row(cls, row) -> 'AttendanceRecord':
        """
        Creates an AttendanceRecord instance from a database row.

        This class method is used to reconstruct an AttendanceRecord object from data
        retrieved from the database. It leverages `BaseModel.from_row`
        for common fields and then populates record-specific attributes.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            AttendanceRecord: An AttendanceRecord instance populated with data from the row,
                              or None if the row is None.
        """
        if row is None:
            return None
        
        # Use BaseModel's from_row to parse common fields.
        base_instance = BaseModel.from_row(row)
        if not base_instance:
            return None

        row_dict = dict(row) # Convert row to dict for easier access to specific fields.
        
        # Extract record-specific fields.
        student_id = row_dict.get('student_id')
        module_id = row_dict.get('module_id')
        week_number = row_dict.get('week_number')
        attended_sessions = row_dict.get('attended_sessions')
        total_sessions = row_dict.get('total_sessions')
        attendance_rate = row_dict.get('attendance_rate')
        student_name = row_dict.get('student_name')
        module_title = row_dict.get('module_title')

        return cls(
            id=base_instance.id,
            student_id=student_id,
            module_id=module_id,
            week_number=week_number,
            attended_sessions=attended_sessions,
            total_sessions=total_sessions,
            attendance_rate=attendance_rate,
            student_name=student_name,
            module_title=module_title,
            is_active=base_instance.is_active,
            created_at=base_instance.created_at
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the AttendanceRecord object, useful for debugging.
        """
        return f'<AttendanceRecord ID: {self.id}, Student: {self.student_id}, Module: {self.module_id}, Week: {self.week_number}>'
