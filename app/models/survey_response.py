from datetime import datetime
from .base_model import BaseModel

class SurveyResponse(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, stress_level=None, hours_slept=None, mood_comment=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.stress_level = stress_level
        self.hours_slept = hours_slept
        self.mood_comment = mood_comment

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'stress_level': self.stress_level,
            'hours_slept': self.hours_slept,
            'mood_comment': self.mood_comment,
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
            stress_level=row_dict.get('stress_level'),
            hours_slept=row_dict.get('hours_slept'),
            mood_comment=row_dict.get('mood_comment'),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<SurveyResponse student={self.student_id} week={self.week_number}>'
