from datetime import datetime
from .base_model import BaseModel

class Alert(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, reason=None, resolved=False, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.reason = reason
        self.resolved = resolved

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'reason': self.reason,
            'resolved': self.resolved,
        })
        return data

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        row_dict = dict(row)
        
        # Parse created_at if it's a string
        created_at_str = row_dict.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str

        return cls(
            id=row_dict.get('id'),
            student_id=row_dict.get('student_id'),
            module_id=row_dict.get('module_id'),
            week_number=row_dict.get('week_number'),
            reason=row_dict.get('reason'),
            resolved=bool(row_dict.get('resolved')),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<Alert student={self.student_id} reason={self.reason}>'
