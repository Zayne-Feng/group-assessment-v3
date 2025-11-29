from datetime import datetime
from .base_model import BaseModel

class Grade(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, assessment_name=None, grade=None, student_name=None, module_title=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.assessment_name = assessment_name
        self.grade = grade
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'assessment_name': self.assessment_name,
            'grade': self.grade,
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
            assessment_name=row_dict.get('assessment_name'),
            grade=row_dict.get('grade'),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<Grade student={self.student_id} assessment={self.assessment_name}>'
