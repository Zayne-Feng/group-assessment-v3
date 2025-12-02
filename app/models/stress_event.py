"""
Stress Event model definition for the application.

This module defines the `StressEvent` class, representing a specific
instance of a student experiencing a high-stress situation. It inherits
from `BaseModel` for common fields and includes attributes for linking
to students and modules, stress level, cause, and source.
"""

from datetime import datetime
from .base_model import BaseModel

class StressEvent(BaseModel):
    """
    Represents a stress event, which is a record of a high-stress situation for a student.

    Inherits from `BaseModel` for common fields such as `id`, `created_at`,
    and `is_active`. These events are typically triggered by survey responses
    or other system detections.
    """
    def __init__(self, id=None, student_id=None, module_id=None, survey_response_id=None, week_number=None, stress_level=None, cause_category=None, description=None, source=None, created_at=None, is_active=True, **kwargs):
        """
        Initializes a StressEvent instance.

        Args:
            id (int, optional): The unique identifier for the stress event.
            student_id (int, optional): The ID of the student experiencing the event.
            module_id (int, optional): The ID of the module related to the event (if applicable).
            survey_response_id (int, optional): The ID of the associated survey response that might have triggered this event.
            week_number (int, optional): The academic week number when the event occurred.
            stress_level (int, optional): The reported or detected stress level during the event.
            cause_category (str, optional): The category of the cause (e.g., 'academic', 'personal').
            description (str, optional): A detailed description of the stress event.
            source (str, optional): The source that identified the stress event (e.g., 'system', 'survey').
            created_at (datetime, optional): The timestamp when the event record was created. Defaults to current UTC time.
            is_active (bool, optional): Whether the event record is active. Defaults to True.
            **kwargs: Additional keyword arguments passed to the BaseModel constructor.
        """
        super().__init__(id=id, created_at=created_at, is_active=is_active, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.survey_response_id = survey_response_id
        self.week_number = week_number
        self.stress_level = stress_level
        self.cause_category = cause_category
        self.description = description
        self.source = source

    def to_dict(self) -> dict:
        """
        Converts the StressEvent object to a dictionary representation, including common base model fields.

        Returns:
            dict: A dictionary containing the stress event's attributes suitable for JSON serialization.
        """
        data = super().to_dict() # Get common fields from BaseModel.
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'survey_response_id': self.survey_response_id,
            'week_number': self.week_number,
            'stress_level': self.stress_level,
            'cause_category': self.cause_category,
            'description': self.description,
            'source': self.source,
        })
        return data

    @classmethod
    def from_row(cls, row) -> 'StressEvent':
        """
        Creates a StressEvent instance from a database row.

        This class method is used to reconstruct a StressEvent object from data
        retrieved from the database. It leverages `BaseModel.from_row`
        for common fields and then populates event-specific attributes.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            StressEvent: A StressEvent instance populated with data from the row,
                         or None if the row is None.
        """
        if row is None:
            return None
        
        # Use BaseModel's from_row to parse common fields.
        base_instance = BaseModel.from_row(row)
        if not base_instance:
            return None

        row_dict = dict(row) # Convert row to dict for easier access to specific fields.

        # Extract stress event-specific fields.
        student_id = row_dict.get('student_id')
        module_id = row_dict.get('module_id')
        survey_response_id = row_dict.get('survey_response_id')
        week_number = row_dict.get('week_number')
        stress_level = row_dict.get('stress_level')
        cause_category = row_dict.get('cause_category')
        description = row_dict.get('description')
        source = row_dict.get('source')

        return cls(
            id=base_instance.id,
            student_id=student_id,
            module_id=module_id,
            survey_response_id=survey_response_id,
            week_number=week_number,
            stress_level=stress_level,
            cause_category=cause_category,
            description=description,
            source=source,
            is_active=base_instance.is_active,
            created_at=base_instance.created_at
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the StressEvent object, useful for debugging.
        """
        return f'<StressEvent ID: {self.id}, Student: {self.student_id}, Level: {self.stress_level}>'
