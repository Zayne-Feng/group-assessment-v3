"""
Base model definition for the application.

This module defines the `BaseModel` class, which provides common attributes
and methods (like ID, active status, creation timestamp, and dictionary conversion)
for all other data models in the application. It also includes a class method
to instantiate a model from a database row, handling common data parsing.
"""

from datetime import datetime, timezone
from flask import current_app # Imported here for logging within from_row, if app context is available

class BaseModel:
    """
    A base model class providing common fields and methods for all other models.

    Attributes:
        id (int): The unique identifier for the record.
        is_active (bool): Indicates whether the record is active (True) or logically deleted (False).
        created_at (datetime): The UTC timestamp when the record was created.
    """
    def __init__(self, id=None, is_active=True, created_at=None):
        """
        Initializes a new instance of the BaseModel.

        Args:
            id (int, optional): The unique identifier for the record. Defaults to None (for new records).
            is_active (bool, optional): The active status of the record. Defaults to True.
            created_at (datetime, optional): The creation timestamp. Defaults to the current UTC time if None.
        """
        self.id = id
        self.is_active = is_active
        # Set created_at to current UTC time if not provided.
        self.created_at = created_at if created_at is not None else datetime.now(timezone.utc)

    def to_dict(self):
        """
        Converts the common fields of the model instance to a dictionary representation.

        This method is designed to be extended by subclasses to include their
        specific attributes.

        Returns:
            dict: A dictionary containing the common attributes (id, is_active, created_at).
        """
        data = {
            'id': self.id,
            'is_active': self.is_active,
            # Convert datetime object to ISO 8601 string for JSON serialization.
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        return data

    @classmethod
    def from_row(cls, row):
        """
        Creates a BaseModel instance (or a subclass instance) from a database row.

        This class method is intended to be called by subclasses' `from_row`
        implementations to handle the parsing of common fields.

        Args:
            row: The database row, expected to be a dict-like object (e.g., `sqlite3.Row`).

        Returns:
            BaseModel: A BaseModel instance (or an instance of the calling subclass)
                       populated with common fields, or None if the input row is None.
        """
        if row is None:
            return None
        
        # Convert sqlite3.Row to a standard dictionary for consistent access.
        row_dict = dict(row)
        
        # Extract common fields from the row dictionary.
        record_id = row_dict.get('id')
        active_status = bool(row_dict.get('is_active', True)) # Default to True if not present.
        
        created_at_parsed = None
        created_at_str = row_dict.get('created_at')
        if created_at_str:
            try:
                # Attempt to parse the ISO 8601 formatted datetime string.
                created_at_parsed = datetime.fromisoformat(created_at_str)
            except ValueError:
                # Log a warning if the datetime string format is invalid.
                # Use current_app.logger if available, otherwise fall back to print.
                if current_app:
                    current_app.logger.warning(
                        f"Invalid datetime format for 'created_at': '{created_at_str}' "
                        f"for record ID {record_id}. Setting to None."
                    )
                else:
                    print(
                        f"WARNING: Invalid datetime format for 'created_at': '{created_at_str}' "
                        f"for record ID {record_id}. Setting to None."
                    )
        
        # Create an instance of the specific model class (cls refers to the subclass).
        # Subclasses will typically call this super method and then handle their
        # specific fields.
        return cls(id=record_id, is_active=active_status, created_at=created_at_parsed)
