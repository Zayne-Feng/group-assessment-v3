from app.db_connection import get_db
from app.models.submission_record import SubmissionRecord
from app.models.student import Student
from app.models.module import Module
from datetime import datetime

class SubmissionRecordRepository:
    @staticmethod
    def get_all_submission_records():
        db = get_db()
        cursor = db.execute("""
            SELECT sr.id, sr.student_id, sr.module_id, sr.assessment_name, sr.due_date, sr.submitted_date, sr.is_submitted, sr.is_late, sr.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM submission_records sr
            JOIN students s ON sr.student_id = s.id
            JOIN modules m ON sr.module_id = m.id
            WHERE sr.is_active = 1
        """)
        records = []
        for row in cursor.fetchall():
            record = SubmissionRecord.from_row(row)
            record.student_name = row['student_name']
            record.module_title = row['module_title']
            records.append(record)
        return records

    @staticmethod
    def get_submission_record_by_id(record_id):
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active FROM submission_records WHERE id = ? AND is_active = 1", (record_id,))
        record = SubmissionRecord.from_row(cursor.fetchone())
        return record

    @staticmethod
    def create_submission_record(student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO submission_records (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
            (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late)
        )
        db.commit()
        return SubmissionRecord(id=cursor.lastrowid, student_id=student_id, module_id=module_id, assessment_name=assessment_name, due_date=due_date, submitted_date=submitted_date, is_submitted=is_submitted, is_late=is_late)

    @staticmethod
    def update_submission_record(record_id, student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late):
        db = get_db()
        db.execute(
            "UPDATE submission_records SET student_id = ?, module_id = ?, assessment_name = ?, due_date = ?, submitted_date = ?, is_submitted = ?, is_late = ? WHERE id = ?",
            (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, record_id)
        )
        db.commit()
        return SubmissionRecordRepository.get_submission_record_by_id(record_id)

    @staticmethod
    def delete_submission_record(record_id):
        db = get_db()
        db.execute("UPDATE submission_records SET is_active = 0 WHERE id = ?", (record_id,))
        db.commit()
        return True
