from app.db_connection import get_db
from app.models.alert import Alert

class AlertRepository:
    @staticmethod
    def get_all_alerts():
        db = get_db()
        # Joining with students and modules to get names, as in the original static implementation
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
            # The original static version returned a dict, not an object with extra attributes.
            # Let's return a dictionary to match the expected output in the original admin/routes.py.
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

    # Adding a create method based on the likely original implementation
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
