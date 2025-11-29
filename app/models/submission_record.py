from datetime import datetime, date
from .base_model import BaseModel

class SubmissionRecord(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, assessment_name=None, due_date=None, submitted_date=None, is_submitted=False, is_late=False, student_name=None, module_title=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.assessment_name = assessment_name
        self.due_date = due_date
        self.submitted_date = submitted_date
        self.is_submitted = is_submitted
        self.is_late = is_late
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'assessment_name': self.assessment_name,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'submitted_date': self.submitted_date.isoformat() if self.submitted_date else None,
            'is_submitted': self.is_submitted,
            'is_late': self.is_late,
            'student_name': self.student_name,
            'module_title': self.module_title
        })
        return data

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        row_dict = dict(row)
        
        # Helper to parse date strings safely
        def parse_date(date_str):
            if not isinstance(date_str, str):
                return date_str
            try:
                return datetime.fromisoformat(date_str)
            except (ValueError, TypeError):
                return None

        # Parse created_at if it's a string
        created_at_str = row_dict.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str

        return cls(
            id=row_dict.get('id'),
            student_id=row_dict.get('student_id'),
            module_id=row_dict.get('module_id'),
            assessment_name=row_dict.get('assessment_name'),
            due_date=parse_date(row_dict.get('due_date')),
            submitted_date=parse_date(row_dict.get('submitted_date')),
            is_submitted=bool(row_dict.get('is_submitted')),
            is_late=bool(row_dict.get('is_late')),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<SubmissionRecord student={self.student_id} assessment={self.assessment_name}>'
