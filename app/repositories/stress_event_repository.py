from app.db_connection import get_db
from app.models.stress_event import StressEvent
from datetime import datetime

class StressEventRepository:
    @staticmethod
    def get_all_stress_events():
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active FROM stress_events WHERE is_active = 1")
        events = [StressEvent.from_row(row) for row in cursor.fetchall()]
        return events

    @staticmethod
    def get_stress_event_by_id(event_id):
        db = get_db()
        cursor = db.execute("SELECT id, student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active FROM stress_events WHERE id = ? AND is_active = 1", (event_id,))
        event = StressEvent.from_row(cursor.fetchone())
        return event

    @staticmethod
    def create_stress_event(student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source):
        db = get_db()
        created_at = datetime.utcnow().isoformat()
        
        cursor = db.execute(
            "INSERT INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
            (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at)
        )
        db.commit()
        return StressEvent(id=cursor.lastrowid, student_id=student_id, module_id=module_id, survey_response_id=survey_response_id, week_number=week_number, stress_level=stress_level, cause_category=cause_category, description=description, source=source, created_at=created_at)

    @staticmethod
    def update_stress_event(event_id, student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source):
        db = get_db()
        db.execute(
            "UPDATE stress_events SET student_id = ?, module_id = ?, survey_response_id = ?, week_number = ?, stress_level = ?, cause_category = ?, description = ?, source = ? WHERE id = ?",
            (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, event_id)
        )
        db.commit()
        return StressEventRepository.get_stress_event_by_id(event_id)

    @staticmethod
    def delete_stress_event(event_id):
        db = get_db()
        db.execute("UPDATE stress_events SET is_active = 0 WHERE id = ?", (event_id,))
        db.commit()
        return True
