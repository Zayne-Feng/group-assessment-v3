from datetime import datetime

class Grade:
    def __init__(self, id=None, student_id=None, module_id=None, assessment_name=None, grade=None, is_active=True):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.assessment_name = assessment_name
        self.grade = grade
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'assessment_name': self.assessment_name,
            'grade': self.grade,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Grade(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            assessment_name=row['assessment_name'],
            grade=row['grade'],
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<Grade student={self.student_id} assessment={self.assessment_name}>'
