from app.db_connection import get_db
from app.models.alert import Alert

class AlertRepository:
    @staticmethod
    def get_all_alerts():
        db = get_db()
        cursor = db.execute("""
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            WHERE a.is_active = 1
            ORDER BY a.created_at DESC
        """)
        alerts = []
        for row in cursor.fetchall():
            alert = Alert.from_row(row)
            alert_dict = alert.to_dict()
            alert_dict['student_name'] = row['student_name']
            alert_dict['module_title'] = row['module_title']
            alerts.append(alert_dict)
        return alerts

    @staticmethod
    def get_recent_alerts_per_student():
        db = get_db()
        cursor = db.execute("""
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            JOIN (
                SELECT student_id, MAX(week_number) AS max_week_number -- Changed to MAX(week_number)
                FROM alerts
                WHERE is_active = 1
                GROUP BY student_id
            ) AS latest_alerts
            ON a.student_id = latest_alerts.student_id AND a.week_number = latest_alerts.max_week_number -- Changed join condition
            WHERE a.is_active = 1
            ORDER BY a.week_number DESC, a.created_at DESC -- Order by week_number, then created_at for tie-breaking
        """)
        alerts = []
        for row in cursor.fetchall():
            alert = Alert.from_row(row)
            alert_dict = alert.to_dict()
            alert_dict['student_name'] = row['student_name']
            alert_dict['module_title'] = row['module_title']
            alerts.append(alert_dict)
        return alerts

    @staticmethod
    def get_alerts_by_student_id(student_id):
        db = get_db()
        cursor = db.execute("""
            SELECT a.id, a.student_id, a.module_id, a.week_number, a.reason, a.created_at, a.resolved, a.is_active,
                   s.full_name AS student_name, m.module_title AS module_title
            FROM alerts a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN modules m ON a.module_id = m.id
            WHERE a.student_id = ? AND a.is_active = 1
            ORDER BY a.created_at DESC
        """, (student_id,))
        alerts = []
        for row in cursor.fetchall():
            alert = Alert.from_row(row)
            alert_dict = alert.to_dict()
            alert_dict['student_name'] = row['student_name']
            alert_dict['module_title'] = row['module_title']
            alerts.append(alert_dict)
        return alerts

    @staticmethod
    def get_alert_by_id(alert_id):
        db = get_db()
        cursor = db.execute("SELECT * FROM alerts WHERE id = ? AND is_active = 1", (alert_id,))
        row = cursor.fetchone()
        return Alert.from_row(row) if row else None

    @staticmethod
    def mark_alert_resolved(alert_id):
        db = get_db()
        db.execute("UPDATE alerts SET resolved = 1 WHERE id = ?", (alert_id,))
        db.commit()
        return True
    
    @staticmethod
    def delete_alert(alert_id):
        db = get_db()
        db.execute("UPDATE alerts SET is_active = 0 WHERE id = ?", (alert_id,))
        db.commit()
        return True

    @staticmethod
    def create_alert(student_id, module_id, week_number, reason):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO alerts (student_id, module_id, week_number, reason, resolved, is_active) VALUES (?, ?, ?, ?, 0, 1)",
            (student_id, module_id, week_number, reason)
        )
        db.commit()
        alert_id = cursor.lastrowid
        return AlertRepository.get_alert_by_id(alert_id)
