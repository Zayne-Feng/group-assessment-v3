from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, id=None, username=None, password_hash=None, role='user', student_id=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.student_id = student_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'username': self.username,
            'role': self.role,
            'student_id': self.student_id,
        })
        return data

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        row_dict = dict(row)
        
        # Handle student_id safely, as it might not exist for all rows or could be None
        student_id = row_dict.get('student_id')

        # Parse created_at if it's a string
        created_at_str = row_dict.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str

        return cls(
            id=row_dict.get('id'),
            username=row_dict.get('username'),
            password_hash=row_dict.get('password_hash'),
            role=row_dict.get('role'),
            student_id=student_id,
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<User {self.username}>'
