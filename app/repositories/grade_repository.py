from app.db_connection import get_db
from app.models.grade import Grade

class GradeRepository:
    @staticmethod
    def get_all_grades():
        db = get_db()
        cursor = db.execute("""
            SELECT g.id, g.student_id, g.module_id, g.assessment_name, g.grade, g.is_active,
                   s.full_name as student_name, m.module_title as module_title
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN modules m ON g.module_id = m.id
            WHERE g.is_active = 1
        """)
        grades = []
        for row in cursor.fetchall():
            grade = Grade.from_row(row)
            grade.student_name = row['student_name']
            grade.module_title = row['module_title']
            grades.append(grade)
        return grades

    @staticmethod
    def get_grade_by_id(grade_id):
        db = get_db()
        cursor = db.execute("SELECT * FROM grades WHERE id = ? AND is_active = 1", (grade_id,))
        row = cursor.fetchone()
        return Grade.from_row(row) if row else None

    @staticmethod
    def create_grade(student_id, module_id, assessment_name, grade):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO grades (student_id, module_id, assessment_name, grade, is_active) VALUES (?, ?, ?, ?, 1)",
            (student_id, module_id, assessment_name, grade)
        )
        db.commit()
        grade_id = cursor.lastrowid
        return GradeRepository.get_grade_by_id(grade_id)

    @staticmethod
    def update_grade(grade_id, student_id, module_id, assessment_name, grade):
        db = get_db()
        db.execute(
            "UPDATE grades SET student_id = ?, module_id = ?, assessment_name = ?, grade = ? WHERE id = ?",
            (student_id, module_id, assessment_name, grade, grade_id)
        )
        db.commit()
        return GradeRepository.get_grade_by_id(grade_id)

    @staticmethod
    def delete_grade(grade_id):
        db = get_db()
        db.execute("UPDATE grades SET is_active = 0 WHERE id = ?", (grade_id,))
        db.commit()
        return True
