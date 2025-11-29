from datetime import datetime
from .base_model import BaseModel

class AttendanceRecord(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, attended_sessions=None, total_sessions=None, attendance_rate=None, student_name=None, module_title=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.attended_sessions = attended_sessions
        self.total_sessions = total_sessions
        self.attendance_rate = attendance_rate
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'attended_sessions': self.attended_sessions,
            'total_sessions': self.total_sessions,
            'attendance_rate': self.attendance_rate,
            'student_name': self.student_name,
            'module_title': self.module_title
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
            attended_sessions=row_dict.get('attended_sessions'),
            total_sessions=row_dict.get('total_sessions'),
            attendance_rate=row_dict.get('attendance_rate'),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<AttendanceRecord student={self.student_id} module={self.module_id} week={self.week_number}>'
