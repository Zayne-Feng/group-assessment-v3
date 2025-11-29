import sqlite3
from app.db_connection import get_db
from app.models.student import Student
from .base_repository import BaseRepository

class StudentRepository(BaseRepository):
    def __init__(self):
        super().__init__('students', Student)

    def get_all_students(self):
        return super().get_all()

    def get_student_by_id(self, student_id):
        return super().get_by_id(student_id)

    def get_student_by_student_number(self, student_number):
        query = "SELECT * FROM students WHERE student_number = ? AND is_active = 1"
        return self._execute_query(query, (student_number,), fetch_one=True)

    def get_student_enrolments(self, student_id):
        query = """
            SELECT e.id, e.student_id, e.module_id, e.enrol_date, e.is_active,
                   m.module_code, m.module_title
            FROM enrolments e
            JOIN modules m ON e.module_id = m.id
            WHERE e.student_id = ? AND e.is_active = 1
        """
        db = get_db()
        try:
            cursor = db.execute(query, (student_id,))
            enrolments = []
            for row in cursor.fetchall():
                enrolments.append({
                    'id': row['id'],
                    'module_id': row['module_id'],
                    'module_code': row['module_code'],
                    'module_title': row['module_title'],
                    'enrol_date': row['enrol_date']
                })
            return enrolments
        except sqlite3.Error as e:
            print(f"Database error in get_student_enrolments: {e}")
            raise Exception(f"Could not retrieve enrolments for student {student_id}.")

    def create_student(self, student_number, full_name, email, course_name, year_of_study):
        query = "INSERT INTO students (student_number, full_name, email, course_name, year_of_study, is_active) VALUES (?, ?, ?, ?, ?, 1)"
        student_id = self._execute_insert(query, (student_number, full_name, email, course_name, year_of_study))
        return self.get_student_by_id(student_id)

    def update_student(self, student_id, student_number, full_name, email, course_name, year_of_study):
        query = "UPDATE students SET student_number = ?, full_name = ?, email = ?, course_name = ?, year_of_study = ? WHERE id = ?"
        self._execute_update_delete(query, (student_number, full_name, email, course_name, year_of_study, student_id))
        return self.get_student_by_id(student_id)

    def delete_student(self, student_id):
        return super().delete_logical(student_id)

    def delete_student_hard(self, student_id):
        return super().delete_hard(student_id)

# Instantiate the repository for use
student_repository = StudentRepository()
