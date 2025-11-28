from app.db_connection import get_db
from app.models.enrolment import Enrolment
from app.models.student import Student
from app.models.module import Module
from datetime import datetime

class EnrolmentRepository:
    @staticmethod
    def get_all_enrolments():
        db = get_db()
        cursor = db.execute("""
            SELECT e.id, e.student_id, e.module_id, e.enrol_date, e.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM enrolments e
            JOIN students s ON e.student_id = s.id
            JOIN modules m ON e.module_id = m.id
            WHERE e.is_active = 1
        """)
        enrolments = []
        for row in cursor.fetchall():
            enrolment = Enrolment.from_row(row)
            enrolment.student_name = row['student_name']
            enrolment.module_title = row['module_title']
            enrolments.append(enrolment)
        return enrolments

    @staticmethod
    def get_enrolment_by_id(enrolment_id):
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, enrol_date, is_active FROM enrolments WHERE id = ? AND is_active = 1", (enrolment_id,))
        enrolment = Enrolment.from_row(cursor.fetchone())
        return enrolment

    @staticmethod
    def create_enrolment(student_id, module_id, enrol_date=None):
        db = get_db()
        if enrol_date is None:
            enrol_date = datetime.utcnow().date().isoformat()
        
        cursor = db.execute(
            "INSERT INTO enrolments (student_id, module_id, enrol_date, is_active) VALUES (?, ?, ?, 1)",
            (student_id, module_id, enrol_date)
        )
        db.commit()
        return Enrolment(id=cursor.lastrowid, student_id=student_id, module_id=module_id, enrol_date=enrol_date)

    @staticmethod
    def update_enrolment(enrolment_id, student_id, module_id, enrol_date):
        db = get_db()
        db.execute(
            "UPDATE enrolments SET student_id = ?, module_id = ?, enrol_date = ? WHERE id = ?",
            (student_id, module_id, enrol_date, enrolment_id)
        )
        db.commit()
        return EnrolmentRepository.get_enrolment_by_id(enrolment_id)

    @staticmethod
    def delete_enrolment(enrolment_id):
        db = get_db()
        db.execute("UPDATE enrolments SET is_active = 0 WHERE id = ?", (enrolment_id,))
        db.commit()
        return True
