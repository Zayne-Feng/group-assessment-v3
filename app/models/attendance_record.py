class AttendanceRecord:
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, attended_sessions=None, total_sessions=None, attendance_rate=None, is_active=True, student_name=None, module_title=None):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.attended_sessions = attended_sessions
        self.total_sessions = total_sessions
        self.attendance_rate = attendance_rate
        self.is_active = is_active
        # For carrying extra data from JOINs
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'attended_sessions': self.attended_sessions,
            'total_sessions': self.total_sessions,
            'attendance_rate': self.attendance_rate,
            'is_active': self.is_active,
            'student_name': self.student_name,
            'module_title': self.module_title
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return AttendanceRecord(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            week_number=row['week_number'],
            attended_sessions=row['attended_sessions'],
            total_sessions=row['total_sessions'],
            attendance_rate=row['attendance_rate'],
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<AttendanceRecord student={self.student_id} module={self.module_id} week={self.week_number}>'
