from datetime import datetime, date

class SubmissionRecord:
    def __init__(self, id=None, student_id=None, module_id=None, assessment_name=None, due_date=None, submitted_date=None, is_submitted=False, is_late=False, is_active=True, student_name=None, module_title=None):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.assessment_name = assessment_name
        self.due_date = due_date
        self.submitted_date = submitted_date
        self.is_submitted = is_submitted
        self.is_late = is_late
        self.is_active = is_active
        # For carrying extra data from JOINs
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'assessment_name': self.assessment_name,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'submitted_date': self.submitted_date.isoformat() if self.submitted_date else None,
            'is_submitted': self.is_submitted,
            'is_late': self.is_late,
            'is_active': self.is_active,
            'student_name': self.student_name,
            'module_title': self.module_title
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        
        # Helper to parse date strings safely
        def parse_date(date_str):
            if not isinstance(date_str, str):
                return date_str
            try:
                return datetime.fromisoformat(date_str)
            except (ValueError, TypeError):
                return None

        return SubmissionRecord(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            assessment_name=row['assessment_name'],
            due_date=parse_date(row['due_date']),
            submitted_date=parse_date(row['submitted_date']),
            is_submitted=bool(row['is_submitted']),
            is_late=bool(row['is_late']),
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<SubmissionRecord student={self.student_id} assessment={self.assessment_name}>'
