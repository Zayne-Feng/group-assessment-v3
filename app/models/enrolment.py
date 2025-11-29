from datetime import datetime, date
from .base_model import BaseModel

class Enrolment(BaseModel):
    def __init__(self, id=None, student_id=None, module_id=None, enrol_date=None, student_name=None, module_title=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.student_id = student_id
        self.module_id = module_id
        self.enrol_date = enrol_date if enrol_date is not None else datetime.utcnow().date()
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        data = super().to_dict()
        # Convert date object to string if it's a date
        enrol_date_str = self.enrol_date
        if isinstance(self.enrol_date, (datetime, date)):
            enrol_date_str = self.enrol_date.isoformat()

        data.update({
            'student_id': self.student_id,
            'module_id': self.module_id,
            'enrol_date': enrol_date_str,
            'student_name': self.student_name,
            'module_title': self.module_title
        })
        return data

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        row_dict = dict(row)
        
        enrol_date_obj = row_dict.get('enrol_date')
        if isinstance(enrol_date_obj, str):
            try:
                enrol_date_obj = datetime.fromisoformat(enrol_date_obj).date()
            except ValueError:
                enrol_date_obj = date.fromisoformat(enrol_date_obj)

        # Parse created_at if it's a string
        created_at_str = row_dict.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str

        return cls(
            id=row_dict.get('id'),
            student_id=row_dict.get('student_id'),
            module_id=row_dict.get('module_id'),
            enrol_date=enrol_date_obj,
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<Enrolment student={self.student_id} module={self.module_id}>'
