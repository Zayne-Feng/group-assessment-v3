from datetime import datetime, date

class Enrolment:
    def __init__(self, id=None, student_id=None, module_id=None, enrol_date=None, is_active=True, student_name=None, module_title=None):
        self.id = id
        self.student_id = student_id
        self.module_id = module_id
        self.enrol_date = enrol_date if enrol_date is not None else datetime.utcnow().date()
        self.is_active = is_active
        # These fields are for carrying extra data from JOINs
        self.student_name = student_name
        self.module_title = module_title

    def to_dict(self):
        # Convert date object to string if it's a date
        enrol_date_str = self.enrol_date
        if isinstance(self.enrol_date, (datetime, date)):
            enrol_date_str = self.enrol_date.isoformat()

        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'enrol_date': enrol_date_str,
            'is_active': self.is_active,
            'student_name': self.student_name,
            'module_title': self.module_title
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        
        enrol_date_obj = row['enrol_date']
        if isinstance(enrol_date_obj, str):
            try:
                # Handles both date and datetime strings
                enrol_date_obj = datetime.fromisoformat(enrol_date_obj).date()
            except ValueError:
                # Handle cases where it might just be a date string
                enrol_date_obj = date.fromisoformat(enrol_date_obj)

        return Enrolment(
            id=row['id'],
            student_id=row['student_id'],
            module_id=row['module_id'],
            enrol_date=enrol_date_obj,
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<Enrolment student={self.student_id} module={self.module_id}>'
