"""
Survey Response model definition for the application.

This module defines the `SurveyResponse` class, representing a student's
response to a wellbeing survey. It inherits from `BaseModel` for common
fields and includes attributes for linking to students and modules,
stress levels, sleep hours, and mood comments.
"""

from datetime import datetime
from .base_model import BaseModel

class SurveyResponse(BaseModel):
    """
    Represents a student's response to a survey.

    Inherits from `BaseModel` for common fields such as `id`, `created_at`,
    and `is_active`. Survey responses are crucial for monitoring student
    wellbeing and identifying potential issues.
    """
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, stress_level=None, hours_slept=None, mood_comment=None, created_at=None, is_active=True, **kwargs):
        """
        Initializes a SurveyResponse instance.

        Args:
            id (int, optional): The unique identifier for the survey response.
            student_id (int, optional): The ID of the student who submitted the response.
            module_id (int, optional): The ID of the module related to the survey (if applicable).
            week_number (int, optional): The academic week number the survey pertains to.
            stress_level (int, optional): The reported stress level (e.g., 1-5).
            hours_slept (float, optional): The reported hours of sleep.
            mood_comment (str, optional): Any additional comments provided by the student about their mood.
            created_at (datetime, optional): The timestamp when the response record was created. Defaults to current UTC time.
            is_active (bool, optional): Whether the record is active. Defaults to True.
            **kwargs: Additional keyword arguments passed to the BaseModel constructor.
        """
        super().__init__(id=id, created_at=created_at, is_active=is_active, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.stress_level = stress_level
        self.hours_slept = hours_slept
        self.mood_comment = mood_comment

    def to_dict(self) -> dict:
        """
        Converts the SurveyResponse object to a dictionary representation, including common base model fields.

        Returns:
            dict: A dictionary containing the survey response's attributes suitable for JSON serialization.
        """
        data = super(SurveyResponse, self).to_dict() # Get common fields from BaseModel.
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'stress_level': self.stress_level,
            'hours_slept': self.hours_slept,
            'mood_comment': self.mood_comment,
        })
        return data

    @classmethod
    def from_row(cls, row) -> 'SurveyResponse':
        """
        Creates a SurveyResponse instance from a database row.

        This class method is used to reconstruct a SurveyResponse object from data
        retrieved from the database. It leverages `BaseModel.from_row`
        for common fields and then populates response-specific attributes.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            SurveyResponse: A SurveyResponse instance populated with data from the row,
                            or None if the row is None.
        """
        if row is None:
            return None
        
        # Use BaseModel's from_row to parse common fields.
        base_instance = BaseModel.from_row(row)
        if not base_instance:
            return None

        row_dict = dict(row) # Convert row to dict for easier access to specific fields.

        # Extract response-specific fields.
        student_id = row_dict.get('student_id')
        module_id = row_dict.get('module_id')
        week_number = row_dict.get('week_number')
        stress_level = row_dict.get('stress_level')
        hours_slept = row_dict.get('hours_slept')
        mood_comment = row_dict.get('mood_comment')

        return cls(
            id=base_instance.id,
            student_id=student_id,
            module_id=module_id,
            week_number=week_number,
            stress_level=stress_level,
            hours_slept=hours_slept,
            mood_comment=mood_comment,
            is_active=base_instance.is_active,
            created_at=base_instance.created_at
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the SurveyResponse object, useful for debugging.
        """
        return f'<SurveyResponse ID: {self.id}, Student: {self.student_id}, Week: {self.week_number}, Stress: {self.stress_level}>'
