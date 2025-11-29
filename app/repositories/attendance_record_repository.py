import sqlite3
from app.db_connection import get_db
from app.models.attendance_record import AttendanceRecord
from .base_repository import BaseRepository

class AttendanceRecordRepository(BaseRepository):
    def __init__(self):
        super().__init__('attendance_records', AttendanceRecord)

    def get_all_attendance_records(self):
        query = """
            SELECT ar.id, ar.student_id, ar.module_id, ar.week_number, ar.attended_sessions, ar.total_sessions, ar.attendance_rate, ar.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM attendance_records ar
            JOIN students s ON ar.student_id = s.id
            JOIN modules m ON ar.module_id = m.id
            WHERE ar.is_active = 1
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_attendance_record_by_id(self, record_id):
        return super().get_by_id(record_id)

    def create_attendance_record(self, student_id, module_id, week_number, attended_sessions, total_sessions):
        attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0
        query = """
            INSERT INTO attendance_records (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """
        record_id = self._execute_insert(query, (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate))
        return self.get_attendance_record_by_id(record_id)

    def update_attendance_record(self, record_id, student_id, module_id, week_number, attended_sessions, total_sessions):
        attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0
        query = """
            UPDATE attendance_records SET student_id = ?, module_id = ?, week_number = ?, attended_sessions = ?, total_sessions = ?, attendance_rate = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, record_id))
        return self.get_attendance_record_by_id(record_id)

    def delete_attendance_record(self, record_id):
        return super().delete_logical(record_id)

# Instantiate the repository for use
attendance_record_repository = AttendanceRecordRepository()
