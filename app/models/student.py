class Student:
    def __init__(self, id=None, student_number=None, full_name=None, email=None, course_name=None, year_of_study=None, is_active=True):
        self.id = id
        self.student_number = student_number
        self.full_name = full_name
        self.email = email
        self.course_name = course_name
        self.year_of_study = year_of_study
        self.is_active = is_active
        # Relationships will be handled by repository methods, not directly in the model

    def to_dict(self):
        return {
            'id': self.id,
            'student_number': self.student_number,
            'full_name': self.full_name,
            'email': self.email,
            'course_name': self.course_name,
            'year_of_study': self.year_of_study,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Student(
            id=row['id'],
            student_number=row['student_number'],
            full_name=row['full_name'],
            email=row['email'],
            course_name=row['course_name'],
            year_of_study=row['year_of_study'],
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<Student {self.full_name}>'
