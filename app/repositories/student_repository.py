from app.db_connection import get_db
from app.models.student import Student
from app.models.enrolment import Enrolment
from app.models.module import Module

class StudentRepository:
    @staticmethod
    def get_all_students():
        db = get_db()
        cursor = db.execute("SELECT id, student_number, full_name, email, course_name, year_of_study, is_active FROM students WHERE is_active = 1")
        students = [Student.from_row(row) for row in cursor.fetchall()]
        return students

    @staticmethod
    def get_student_by_id(student_id):
        db = get_db()
        cursor = db.execute("SELECT id, student_number, full_name, email, course_name, year_of_study, is_active FROM students WHERE id = ? AND is_active = 1", (student_id,))
        student = Student.from_row(cursor.fetchone())
        return student

    @staticmethod
    def get_student_enrolments(student_id):
        db = get_db()
        cursor = db.execute("""
            SELECT e.id, e.student_id, e.module_id, e.enrol_date, e.is_active,
                   m.module_code, m.module_title
            FROM enrolments e
            JOIN modules m ON e.module_id = m.id
            WHERE e.student_id = ? AND e.is_active = 1
        """, (student_id,))
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

    @staticmethod
    def create_student(student_number, full_name, email, course_name, year_of_study):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO students (student_number, full_name, email, course_name, year_of_study, is_active) VALUES (?, ?, ?, ?, ?, 1)",
            (student_number, full_name, email, course_name, year_of_study)
        )
        db.commit()
        return Student(id=cursor.lastrowid, student_number=student_number, full_name=full_name, email=email, course_name=course_name, year_of_study=year_of_study)

    @staticmethod
    def update_student(student_id, student_number, full_name, email, course_name, year_of_study):
        db = get_db()
        db.execute(
            "UPDATE students SET student_number = ?, full_name = ?, email = ?, course_name = ?, year_of_study = ? WHERE id = ?",
            (student_number, full_name, email, course_name, year_of_study, student_id)
        )
        db.commit()
        return StudentRepository.get_student_by_id(student_id)

    @staticmethod
    def delete_student(student_id):
        db = get_db()
        db.execute("UPDATE students SET is_active = 0 WHERE id = ?", (student_id,))
        db.commit()
        return True
