"""
Enrolment model definition for the application.

This module defines the `Enrolment` class, representing a student's
registration in a specific module. It inherits from `BaseModel` for
common fields and includes attributes for linking students and modules,
along with the enrolment date.
"""

from datetime import datetime, date, timezone
from .base_model import BaseModel
from flask import current_app # Imported here for logging within from_row, if app context is available

class Enrolment(BaseModel):
    """
    Represents the enrolment of a student in a module.

    Inherits from `BaseModel` for common fields such as `id`, `created_at`,
    and `is_active`. It establishes a many-to-many relationship between
    students and modules.
    """
    def __init__(self, id=None, student_id=None, module_id=None, enrol_date=None, student_name=None, module_title=None, created_at=None, is_active=True, **kwargs):
        """
        Initializes an Enrolment instance.

        Args:
            id (int, optional): The unique identifier for the enrolment record.
            student_id (int, optional): The ID of the student who is enrolled.
            module_id (int, optional): The ID of the module in which the student is enrolled.
            enrol_date (date or str, optional): The date of enrolment. Defaults to the current UTC date if None.
            student_name (str, optional): The full name of the student (often populated via JOINs).
            module_title (str, optional): The title of the module (often populated via JOINs).
            created_at (datetime, optional): The timestamp when the record was created. Defaults to current UTC time.
            is_active (bool, optional): Whether the record is active. Defaults to True.
            **kwargs: Additional keyword arguments passed to the BaseModel constructor.
        """
        super().__init__(id=id, created_at=created_at, is_active=is_active, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        # Ensure enrol_date is a date object, defaulting to current UTC date.
        if isinstance(enrol_date, str):
            try:
                self.enrol_date = datetime.fromisoformat(enrol_date).date()
            except ValueError:
                self.enrol_date = date.fromisoformat(enrol_date) # Fallback for date-only string
        elif enrol_date is None:
            self.enrol_date = datetime.now(timezone.utc).date()
        else:
            self.enrol_date = enrol_date
        
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self) -> dict:
        """
        Converts the Enrolment object to a dictionary representation, including common base model fields.

        Returns:
            dict: A dictionary containing the enrolment's attributes suitable for JSON serialization.
        """
        data = super().to_dict() # Get common fields from BaseModel.
        # Convert date object to ISO 8601 string for JSON serialization.
        enrol_date_str = self.enrol_date.isoformat() if isinstance(self.enrol_date, (datetime, date)) else self.enrol_date

        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'enrol_date': enrol_date_str,
            'student_name': self.student_name,
            'module_title': self.module_title
        })
        return data

    @classmethod
    def from_row(cls, row) -> 'Enrolment':
        """
        Creates an Enrolment instance from a database row.

        This class method is used to reconstruct an Enrolment object from data
        retrieved from the database. It leverages `BaseModel.from_row`
        for common fields and then populates enrolment-specific attributes.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            Enrolment: An Enrolment instance populated with data from the row,
                       or None if the row is None.
        """
        if row is None:
            return None
        
        # Use BaseModel's from_row to parse common fields.
        base_instance = BaseModel.from_row(row)
        if not base_instance:
            return None

        row_dict = dict(row) # Convert row to dict for easier access to specific fields.
        
        # Extract enrolment-specific fields.
        student_id = row_dict.get('student_id')
        module_id = row_dict.get('module_id')
        
        enrol_date_obj = None
        enrol_date_str = row_dict.get('enrol_date')
        if enrol_date_str:
            try:
                enrol_date_obj = datetime.fromisoformat(enrol_date_str).date()
            except ValueError:
                # Fallback for date-only string if fromisoformat fails on full datetime string.
                try:
                    enrol_date_obj = date.fromisoformat(enrol_date_str)
                except ValueError:
                    if current_app:
                        current_app.logger.warning(
                            f"Invalid date format for 'enrol_date': '{enrol_date_str}' "
                            f"for enrolment ID {row_dict.get('id')}. Setting to None."
                        )
                    else:
                        print(
                            f"WARNING: Invalid date format for 'enrol_date': '{enrol_date_str}' "
                            f"for enrolment ID {row_dict.get('id')}. Setting to None."
                        )

        student_name = row_dict.get('student_name')
        module_title = row_dict.get('module_title')

        return cls(
            id=base_instance.id,
            student_id=student_id,
            module_id=module_id,
            enrol_date=enrol_date_obj,
            student_name=student_name,
            module_title=module_title,
            is_active=base_instance.is_active,
            created_at=base_instance.created_at
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Enrolment object, useful for debugging.
        """
        return f'<Enrolment ID: {self.id}, Student: {self.student_id}, Module: {self.module_id}>'
