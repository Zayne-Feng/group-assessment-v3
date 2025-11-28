from datetime import datetime

class SubmissionRecord:
    def __init__(self, id=None, student_id=None, module_id=None, assessment_name=None, due_date=None, submitted_date=None, is_submitted=False, is_late=False, is_active=True):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.assessment_name = assessment_name
        self.due_date = due_date
        self.submitted_date = submitted_date
        self.is_submitted = is_submitted
        self.is_late = is_late
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'assessment_name': self.assessment_name,
            'due_date': self.due_date.isoformat() if isinstance(self.due_date, datetime) else self.due_date,
            'submitted_date': self.submitted_date.isoformat() if isinstance(self.submitted_date, datetime) else self.submitted_date,
            'is_submitted': self.is_submitted,
            'is_late': self.is_late,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return SubmissionRecord(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            assessment_name=row['assessment_name'],
            due_date=datetime.fromisoformat(row['due_date']) if isinstance(row['due_date'], str) else row['due_date'],
            submitted_date=datetime.fromisoformat(row['submitted_date']) if isinstance(row['submitted_date'], str) else row['submitted_date'],
            is_submitted=bool(row['is_submitted']),
            is_late=bool(row['is_late']),
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<SubmissionRecord student={self.student_id} assessment={self.assessment_name}>'
