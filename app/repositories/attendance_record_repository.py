from app.db_connection import get_db
from app.models.attendance_record import AttendanceRecord
from app.models.student import Student
from app.models.module import Module
from datetime import datetime

class AttendanceRecordRepository:
    @staticmethod
    def get_all_attendance_records():
        db = get_db()
        cursor = db.execute("""
            SELECT ar.id, ar.student_id, ar.module_id, ar.week_number, ar.attended_sessions, ar.total_sessions, ar.attendance_rate, ar.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM attendance_records ar
            JOIN students s ON ar.student_id = s.id
            JOIN modules m ON ar.module_id = m.id
            WHERE ar.is_active = 1
        """)
        records = []
        for row in cursor.fetchall():
            record = AttendanceRecord.from_row(row)
            record.student_name = row['student_name']
            record.module_title = row['module_title']
            records.append(record)
        return records

    @staticmethod
    def get_attendance_record_by_id(record_id):
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active FROM attendance_records WHERE id = ? AND is_active = 1", (record_id,))
        record = AttendanceRecord.from_row(cursor.fetchone())
        return record

    @staticmethod
    def create_attendance_record(student_id, module_id, week_number, attended_sessions, total_sessions):
        db = get_db()
        attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0
        
        cursor = db.execute(
            "INSERT INTO attendance_records (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active) VALUES (?, ?, ?, ?, ?, ?, 1)",
            (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate)
        )
        db.commit()
        return AttendanceRecord(id=cursor.lastrowid, student_id=student_id, module_id=module_id, week_number=week_number, attended_sessions=attended_sessions, total_sessions=total_sessions, attendance_rate=attendance_rate)

    @staticmethod
    def update_attendance_record(record_id, student_id, module_id, week_number, attended_sessions, total_sessions):
        db = get_db()
        attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0
        
        db.execute(
            "UPDATE attendance_records SET student_id = ?, module_id = ?, week_number = ?, attended_sessions = ?, total_sessions = ?, attendance_rate = ? WHERE id = ?",
            (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, record_id)
        )
        db.commit()
        return AttendanceRecordRepository.get_attendance_record_by_id(record_id)

    @staticmethod
    def delete_attendance_record(record_id):
        db = get_db()
        db.execute("UPDATE attendance_records SET is_active = 0 WHERE id = ?", (record_id,))
        db.commit()
        return True
