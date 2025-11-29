import sqlite3
from app.db_connection import get_db
from app.models.alert import Alert
from .base_repository import BaseRepository

class AlertRepository(BaseRepository):
    def __init__(self):
        super().__init__('alerts', Alert)

    def get_all_alerts(self):
        query = """
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            WHERE a.is_active = 1
            ORDER BY a.created_at DESC
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_recent_alerts_per_student(self):
        query = """
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            JOIN (
                SELECT student_id, MAX(week_number) AS max_week_number
                FROM alerts
                WHERE is_active = 1
                GROUP BY student_id
            ) AS latest_alerts
            ON a.student_id = latest_alerts.student_id AND a.week_number = latest_alerts.max_week_number
            WHERE a.is_active = 1
            ORDER BY a.week_number DESC, a.created_at DESC
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_alerts_by_student_id(self, student_id):
        query = """
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            WHERE a.student_id = ? AND a.is_active = 1
            ORDER BY a.created_at DESC
        """
        return self._execute_query(query, (student_id,), fetch_all_dicts=True)

    def get_alert_by_id(self, alert_id):
        return super().get_by_id(alert_id)

    def mark_alert_resolved(self, alert_id):
        query = "UPDATE alerts SET resolved = 1 WHERE id = ?"
        return self._execute_update_delete(query, (alert_id,))
    
    def delete_alert(self, alert_id):
        return super().delete_logical(alert_id)

    def create_alert(self, student_id, module_id, week_number, reason):
        query = "INSERT INTO alerts (student_id, module_id, week_number, reason, resolved, is_active) VALUES (?, ?, ?, ?, 0, 1)"
        alert_id = self._execute_insert(query, (student_id, module_id, week_number, reason))
        return self.get_alert_by_id(alert_id)

# Instantiate the repository for use
alert_repository = AlertRepository()
