from datetime import datetime

class BaseModel:
    def __init__(self, id=None, is_active=True, created_at=None):
        self.id = id
        self.is_active = is_active
        self.created_at = created_at if created_at is not None else datetime.utcnow()

    def to_dict(self):
        # Base implementation for common fields
        data = {
            'id': self.id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        return data

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        
        # Convert sqlite3.Row to dict for easier access
        row_dict = dict(row)
        
        # Extract common fields
        id = row_dict.get('id')
        is_active = bool(row_dict.get('is_active', True))
        created_at_str = row_dict.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str

        # Create an instance of the specific model class
        # Subclasses will need to handle their specific fields
        return cls(id=id, is_active=is_active, created_at=created_at)
