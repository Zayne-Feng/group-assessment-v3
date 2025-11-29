import sqlite3
from app.db_connection import get_db
from app.models.stress_event import StressEvent
from datetime import datetime
from .base_repository import BaseRepository

class StressEventRepository(BaseRepository):
    def __init__(self):
        super().__init__('stress_events', StressEvent)

    def get_all_stress_events(self):
        return super().get_all()

    def get_stress_event_by_id(self, event_id):
        return super().get_by_id(event_id)

    def create_stress_event(self, student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source):
        created_at = datetime.utcnow().isoformat()
        query = """
            INSERT INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """
        event_id = self._execute_insert(query, (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at))
        return self.get_stress_event_by_id(event_id)

    def update_stress_event(self, event_id, student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source):
        query = """
            UPDATE stress_events SET student_id = ?, module_id = ?, survey_response_id = ?, week_number = ?, stress_level = ?, cause_category = ?, description = ?, source = ? 
            WHERE id = ?
        """
        self._execute_update_delete(query, (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, event_id))
        return self.get_stress_event_by_id(event_id)

    def delete_stress_event(self, event_id):
        return super().delete_logical(event_id)

# Instantiate the repository for use
stress_event_repository = StressEventRepository()
