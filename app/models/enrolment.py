from datetime import datetime

class Enrolment:
    def __init__(self, id=None, student_id=None, module_id=None, enrol_date=None, is_active=True):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.enrol_date = enrol_date if enrol_date is not None else datetime.utcnow().date()
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'enrol_date': self.enrol_date.isoformat() if isinstance(self.enrol_date, datetime) else self.enrol_date,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Enrolment(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            enrol_date=datetime.fromisoformat(row['enrol_date']) if isinstance(row['enrol_date'], str) else row['enrol_date'],
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<Enrolment student={self.student_id} module={self.module_id}>'
