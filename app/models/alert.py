from datetime import datetime

class Alert:
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, reason=None, created_at=None, resolved=False, is_active=True):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.reason = reason
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.resolved = resolved
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'resolved': self.resolved,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Alert(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            week_number=row['week_number'],
            reason=row['reason'],
            created_at=datetime.fromisoformat(row['created_at']) if isinstance(row['created_at'], str) else row['created_at'],
            resolved=bool(row['resolved']),
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<Alert student={self.student_id} reason={self.reason}>'
