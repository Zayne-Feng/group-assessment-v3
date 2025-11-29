import sqlite3
from app.db_connection import get_db
from app.models.grade import Grade
from .base_repository import BaseRepository

class GradeRepository(BaseRepository):
    def __init__(self):
        super().__init__('grades', Grade)

    def get_all_grades(self):
        query = """
            SELECT g.id, g.student_id, g.module_id, g.assessment_name, g.grade, g.is_active,
                   s.full_name as student_name, m.module_title as module_title
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN modules m ON g.module_id = m.id
            WHERE g.is_active = 1
        """
        return self._execute_query(query, fetch_all_dicts=True)

    def get_grade_by_id(self, grade_id):
        return super().get_by_id(grade_id)

    def create_grade(self, student_id, module_id, assessment_name, grade):
        query = "INSERT INTO grades (student_id, module_id, assessment_name, grade, is_active) VALUES (?, ?, ?, ?, 1)"
        grade_id = self._execute_insert(query, (student_id, module_id, assessment_name, grade))
        return self.get_grade_by_id(grade_id)

    def update_grade(self, grade_id, student_id, module_id, assessment_name, grade):
        query = "UPDATE grades SET student_id = ?, module_id = ?, assessment_name = ?, grade = ? WHERE id = ?"
        self._execute_update_delete(query, (student_id, module_id, assessment_name, grade, grade_id))
        return self.get_grade_by_id(grade_id)

    def delete_grade(self, grade_id):
        return super().delete_logical(grade_id)

# Instantiate the repository for use
grade_repository = GradeRepository()
