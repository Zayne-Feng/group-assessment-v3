from datetime import datetime
from .base_model import BaseModel

class Student(BaseModel):
    def __init__(self, id=None, student_number=None, full_name=None, email=None, course_name=None, year_of_study=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_number = student_number
        self.full_name = full_name
        self.email = email
        self.course_name = course_name
        self.year_of_study = year_of_study

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_number': self.student_number,
            'full_name': self.full_name,
            'email': self.email,
            'course_name': self.course_name,
            'year_of_study': self.year_of_study,
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
            student_number=row_dict.get('student_number'),
            full_name=row_dict.get('full_name'),
            email=row_dict.get('email'),
            course_name=row_dict.get('course_name'),
            year_of_study=row_dict.get('year_of_study'),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<Student {self.full_name}>'
