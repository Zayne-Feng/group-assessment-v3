from datetime import datetime
from .base_model import BaseModel

class StressEvent(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, survey_response_id=None, week_number=None, stress_level=None, cause_category=None, description=None, source=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.survey_response_id = survey_response_id
        self.week_number = week_number
        self.stress_level = stress_level
        self.cause_category = cause_category
        self.description = description
        self.source = source

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'survey_response_id': self.survey_response_id,
            'week_number': self.week_number,
            'stress_level': self.stress_level,
            'cause_category': self.cause_category,
            'description': self.description,
            'source': self.source,
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
            survey_response_id=row_dict.get('survey_response_id'),
            week_number=row_dict.get('week_number'),
            stress_level=row_dict.get('stress_level'),
            cause_category=row_dict.get('cause_category'),
            description=row_dict.get('description'),
            source=row_dict.get('source'),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<StressEvent student={self.student_id} week={self.week_number}>'
