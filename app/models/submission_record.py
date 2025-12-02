"""
Submission Record model definition for the application.

This module defines the `SubmissionRecord` class, representing a student's
submission status for a particular assessment. It inherits from `BaseModel`
for common fields and includes attributes for linking students and modules,
assessment details, due dates, and submission status (submitted, late).
"""

from datetime import datetime, date
from .base_model import BaseModel
from flask import current_app # Imported here for logging within from_row, if app context is available

class SubmissionRecord(BaseModel):
    """
    Represents a submission record for a student's assessment.

    Inherits from `BaseModel` for common fields such as `id`, `created_at`,
    and `is_active`. It tracks whether an assessment was submitted, when,
    and if it was late.
    """
    def __init__(self, id=None, student_id=None, module_id=None, assessment_name=None, due_date=None, submitted_date=None, is_submitted=False, is_late=False, student_name=None, module_title=None, created_at=None, is_active=True, **kwargs):
        """
        Initializes a SubmissionRecord instance.

        Args:
            id (int, optional): The unique identifier for the submission record.
            student_id (int, optional): The ID of the student who made the submission.
            module_id (int, optional): The ID of the module to which the assessment belongs.
            assessment_name (str, optional): The name or description of the assessment.
            due_date (datetime or str, optional): The official due date of the assessment.
            submitted_date (datetime or str, optional): The actual date and time the assessment was submitted.
            is_submitted (bool, optional): True if the assessment was submitted, False otherwise. Defaults to False.
            is_late (bool, optional): True if the submission was late, False otherwise. Defaults to False.
            student_name (str, optional): The full name of the student (often populated via JOINs).
            module_title (str, optional): The title of the module (often populated via JOINs).
            created_at (datetime, optional): The timestamp when the record was created. Defaults to current UTC time.
            is_active (bool, optional): Whether the record is active. Defaults to True.
            **kwargs: Additional keyword arguments passed to the BaseModel constructor.
        """
        super().__init__(id=id, created_at=created_at, is_active=is_active, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.assessment_name = assessment_name
        
        # Safely parse date strings to datetime objects if provided.
        self.due_date = self._parse_date_field(due_date, 'due_date')
        self.submitted_date = self._parse_date_field(submitted_date, 'submitted_date')
        
        self.is_submitted = is_submitted
        self.is_late = is_late
        self.student_name = student_name
        self.module_title = module_title

    def _parse_date_field(self, date_value, field_name: str):
        """Helper to parse date/datetime strings safely."""
        if isinstance(date_value, str):
            try:
                return datetime.fromisoformat(date_value)
            except (ValueError, TypeError):
                if current_app:
                    current_app.logger.warning(
                        f"Invalid datetime format for '{field_name}': '{date_value}'. Setting to None."
                    )
                else:
                    print(f"WARNING: Invalid datetime format for '{field_name}': '{date_value}'. Setting to None.")
                return None
        return date_value

    def to_dict(self) -> dict:
        """
        Converts the SubmissionRecord object to a dictionary representation, including common base model fields.

        Returns:
            dict: A dictionary containing the submission record's attributes suitable for JSON serialization.
        """
        data = super().to_dict() # Get common fields from BaseModel.
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'assessment_name': self.assessment_name,
            # Convert datetime objects to ISO 8601 strings for JSON serialization.
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'submitted_date': self.submitted_date.isoformat() if self.submitted_date else None,
            'is_submitted': self.is_submitted,
            'is_late': self.is_late,
            'student_name': self.student_name,
            'module_title': self.module_title
        })
        return data

    @classmethod
    def from_row(cls, row) -> 'SubmissionRecord':
        """
        Creates a SubmissionRecord instance from a database row.

        This class method is used to reconstruct a SubmissionRecord object from data
        retrieved from the database. It leverages `BaseModel.from_row`
        for common fields and then populates record-specific attributes.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            SubmissionRecord: A SubmissionRecord instance populated with data from the row,
                              or None if the row is None.
        """
        if row is None:
            return None
        
        # Use BaseModel's from_row to parse common fields.
        base_instance = BaseModel.from_row(row)
        if not base_instance:
            return None

        row_dict = dict(row) # Convert row to dict for easier access to specific fields.
        
        # Helper to parse date strings safely within from_row.
        def _parse_date_from_row(date_str_value, field_name):
            if not isinstance(date_str_value, str):
                return date_str_value
            try:
                return datetime.fromisoformat(date_str_value)
            except (ValueError, TypeError):
                if current_app:
                    current_app.logger.warning(
                        f"Invalid datetime format for '{field_name}': '{date_str_value}' "
                        f"for record ID {row_dict.get('id')}. Setting to None."
                    )
                else:
                    print(
                        f"WARNING: Invalid datetime format for '{field_name}': '{date_str_value}' "
                        f"for record ID {row_dict.get('id')}. Setting to None."
                    )
                return None

        # Extract record-specific fields.
        student_id = row_dict.get('student_id')
        module_id = row_dict.get('module_id')
        assessment_name = row_dict.get('assessment_name')
        
        due_date = _parse_date_from_row(row_dict.get('due_date'), 'due_date')
        submitted_date = _parse_date_from_row(row_dict.get('submitted_date'), 'submitted_date')
        
        is_submitted = bool(row_dict.get('is_submitted'))
        is_late = bool(row_dict.get('is_late'))
        student_name = row_dict.get('student_name')
        module_title = row_dict.get('module_title')

        return cls(
            id=base_instance.id,
            student_id=student_id,
            module_id=module_id,
            assessment_name=assessment_name,
            due_date=due_date,
            submitted_date=submitted_date,
            is_submitted=is_submitted,
            is_late=is_late,
            student_name=student_name,
            module_title=module_title,
            is_active=base_instance.is_active,
            created_at=base_instance.created_at
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the SubmissionRecord object, useful for debugging.
        """
        return f'<SubmissionRecord ID: {self.id}, Student: {self.student_id}, Assessment: "{self.assessment_name}">'
