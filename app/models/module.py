"""
Module model definition for the application.

This module defines the `Module` class, representing an academic course
or unit offered within the system. It inherits from `BaseModel` for
common fields and includes attributes for module identification, title,
credit value, and academic year.
"""

from datetime import datetime
from .base_model import BaseModel

class Module(BaseModel):
    """
    Represents a module or course in the system.

    Inherits from `BaseModel` for common fields such as `id`, `created_at`,
    and `is_active`. Modules are fundamental entities for student enrolments
    and academic tracking.
    """
    def __init__(self, id=None, module_code=None, module_title=None, credit=None, academic_year=None, created_at=None, is_active=True, **kwargs):
        """
        Initializes a Module instance.

        Args:
            id (int, optional): The unique identifier for the module.
            module_code (str, optional): The unique code for the module (e.g., 'CS101', 'AI203').
            module_title (str, optional): The full title or name of the module.
            credit (int, optional): The credit value associated with the module.
            academic_year (str, optional): The academic year in which the module is offered (e.g., '2023/2024').
            created_at (datetime, optional): The timestamp when the module record was created. Defaults to current UTC time.
            is_active (bool, optional): Whether the module is currently active. Defaults to True.
            **kwargs: Additional keyword arguments passed to the BaseModel constructor.
        """
        super().__init__(id=id, created_at=created_at, is_active=is_active, **kwargs)
        self.module_code = module_code
        self.module_title = module_title
        self.credit = credit
        self.academic_year = academic_year

    def to_dict(self) -> dict:
        """
        Converts the Module object to a dictionary representation, including common base model fields.

        Returns:
            dict: A dictionary containing the module's attributes suitable for JSON serialization.
        """
        data = super().to_dict() # Get common fields from BaseModel.
        data.update({
            'module_code': self.module_code,
            'module_title': self.module_title,
            'credit': self.credit,
            'academic_year': self.academic_year,
        })
        return data

    @classmethod
    def from_row(cls, row) -> 'Module':
        """
        Creates a Module instance from a database row.

        This class method is used to reconstruct a Module object from data
        retrieved from the database. It leverages `BaseModel.from_row`
        for common fields and then populates module-specific attributes.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            Module: A Module instance populated with data from the row, or None if the row is None.
        """
        if row is None:
            return None
        
        # Use BaseModel's from_row to parse common fields.
        base_instance = BaseModel.from_row(row)
        if not base_instance:
            return None

        row_dict = dict(row) # Convert row to dict for easier access to specific fields.

        # Extract module-specific fields.
        module_code = row_dict.get('module_code')
        module_title = row_dict.get('module_title')
        credit = row_dict.get('credit')
        academic_year = row_dict.get('academic_year')

        return cls(
            id=base_instance.id,
            module_code=module_code,
            module_title=module_title,
            credit=credit,
            academic_year=academic_year,
            is_active=base_instance.is_active,
            created_at=base_instance.created_at
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Module object, useful for debugging.
        """
        return f'<Module ID: {self.id}, Code: {self.module_code}, Title: "{self.module_title}">'
