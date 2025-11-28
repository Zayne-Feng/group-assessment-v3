from datetime import datetime

class SurveyResponse:
    def __init__(self, id=None, student_id=None, module_id=None, week_number=None, stress_level=None, hours_slept=None, mood_comment=None, created_at=None, is_active=True):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.week_number = week_number
        self.stress_level = stress_level
        self.hours_slept = hours_slept
        self.mood_comment = mood_comment
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'week_number': self.week_number,
            'stress_level': self.stress_level,
            'hours_slept': self.hours_slept,
            'mood_comment': self.mood_comment,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return SurveyResponse(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            week_number=row['week_number'],
            stress_level=row['stress_level'],
            hours_slept=row['hours_slept'],
            mood_comment=row['mood_comment'],
            created_at=datetime.fromisoformat(row['created_at']) if isinstance(row['created_at'], str) else row['created_at'],
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<SurveyResponse student={self.student_id} week={self.week_number}>'
