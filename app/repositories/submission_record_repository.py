import sqlite3
from app.db_connection import get_db
from app.models.submission_record import SubmissionRecord
from .base_repository import BaseRepository

class SubmissionRecordRepository(BaseRepository):
    def __init__(self):
        super().__init__('submission_records', SubmissionRecord)

    def get_all_submission_records(self):
        query = """
            SELECT sr.id, sr.student_id, sr.module_id, sr.assessment_name, sr.due_date, sr.submitted_date, sr.is_submitted, sr.is_late, sr.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM submission_records sr
            JOIN students s ON sr.student_id = s.id
            JOIN modules m ON sr.module_id = m.id
            WHERE sr.is_active = 1
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_submission_record_by_id(self, record_id):
        return super().get_by_id(record_id)

    def create_submission_record(self, student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late):
        query = """
            INSERT INTO submission_records (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """
        record_id = self._execute_insert(query, (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late))
        return self.get_submission_record_by_id(record_id)

    def update_submission_record(self, record_id, student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late):
        query = """
            UPDATE submission_records SET student_id = ?, module_id = ?, assessment_name = ?, due_date = ?, submitted_date = ?, is_submitted = ?, is_late = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, record_id))
        return self.get_submission_record_by_id(record_id)

    def delete_submission_record(self, record_id):
        return super().delete_logical(record_id)

# Instantiate the repository for use
submission_record_repository = SubmissionRecordRepository()
