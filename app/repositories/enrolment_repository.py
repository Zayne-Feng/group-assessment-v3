import sqlite3
from app.db_connection import get_db
from app.models.enrolment import Enrolment
from datetime import datetime
from .base_repository import BaseRepository

class EnrolmentRepository(BaseRepository):
    def __init__(self):
        super().__init__('enrolments', Enrolment)

    def get_all_enrolments(self):
        query = """
            SELECT e.id, e.student_id, e.module_id, e.enrol_date, e.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM enrolments e
            JOIN students s ON e.student_id = s.id
            JOIN modules m ON e.module_id = m.id
            WHERE e.is_active = 1
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_enrolment_by_id(self, enrolment_id):
        return super().get_by_id(enrolment_id)

    def create_enrolment(self, student_id, module_id, enrol_date=None):
        if enrol_date is None:
            enrol_date = datetime.utcnow().date().isoformat()
        query = "INSERT INTO enrolments (student_id, module_id, enrol_date, is_active) VALUES (?, ?, ?, 1)"
        enrolment_id = self._execute_insert(query, (student_id, module_id, enrol_date))
        return self.get_enrolment_by_id(enrolment_id)

    def update_enrolment(self, enrolment_id, student_id, module_id, enrol_date):
        query = "UPDATE enrolments SET student_id = ?, module_id = ?, enrol_date = ? WHERE id = ?"
        self._execute_update_delete(query, (student_id, module_id, enrol_date, enrolment_id))
        return self.get_enrolment_by_id(enrolment_id)

    def delete_enrolment(self, enrolment_id):
        return super().delete_logical(enrolment_id)

# Instantiate the repository for use
enrolment_repository = EnrolmentRepository()
