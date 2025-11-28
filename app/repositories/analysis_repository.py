from app.db_connection import get_db
from app.models.survey_response import SurveyResponse
from app.models.attendance_record import AttendanceRecord
from app.models.grade import Grade
from app.models.student import Student
from app.models.module import Module
from app.models.alert import Alert
from app.models.submission_record import SubmissionRecord
from datetime import datetime

class AnalysisRepository:
    @staticmethod
    def get_stress_trend_for_student(student_id):
        db = get_db()
        cursor = db.execute("""
            SELECT week_number, AVG(stress_level) as average_stress_level FROM survey_responses
            WHERE student_id = ? AND is_active = 1
            GROUP BY week_number
            ORDER BY week_number
        """, (student_id,))
        records = cursor.fetchall()
        
        return {
            'labels': [f"Week {row['week_number']}" for row in records],
            'data': [round(row['average_stress_level'], 2) for row in records]
        }

    @staticmethod
    def get_attendance_trend_for_student(student_id):
        db = get_db()
        cursor = db.execute("""
            SELECT week_number, AVG(attendance_rate) as average_attendance_rate FROM attendance_records
            WHERE student_id = ? AND is_active = 1
            GROUP BY week_number
            ORDER BY week_number
        """, (student_id,))
        records = cursor.fetchall()
        
        return {
            'labels': [f"Week {row['week_number']}" for row in records],
            'data': [round(row['average_attendance_rate'] * 100, 2) if row['average_attendance_rate'] is not None else 0 for row in records]
        }

    @staticmethod
    def get_grade_distribution():
        db = get_db()
        grade_bands = {
            'Fail (<40)': 0, 'Pass (40-49)': 0, 'Merit (50-59)': 0,
            'Distinction (60-69)': 0, 'Excellent (70+)': 0
        }
        
        cursor = db.execute("""
            SELECT s.id, AVG(g.grade) AS average_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.is_active = 1 AND g.is_active = 1
            GROUP BY s.id
        """)
        avg_grades = cursor.fetchall()

        for row in avg_grades:
            avg_grade = row['average_grade']
            if avg_grade is None: continue
            if avg_grade < 40: grade_bands['Fail (<40)'] += 1
            elif 40 <= avg_grade < 50: grade_bands['Pass (40-49)'] += 1
            elif 50 <= avg_grade < 60: grade_bands['Merit (50-59)'] += 1
            elif 60 <= avg_grade < 70: grade_bands['Distinction (60-69)'] += 1
            else: grade_bands['Excellent (70+)'] += 1
        
        return {'labels': list(grade_bands.keys()), 'data': list(grade_bands.values())}

    @staticmethod
    def get_stress_grade_correlation():
        db = get_db()
        cursor = db.execute("""
            SELECT s.full_name, AVG(sr.stress_level) AS average_stress, AVG(g.grade) AS average_grade
            FROM students s
            LEFT JOIN survey_responses sr ON s.id = sr.student_id AND sr.is_active = 1
            LEFT JOIN grades g ON s.id = g.student_id AND g.is_active = 1
            WHERE s.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING average_stress IS NOT NULL AND average_grade IS NOT NULL
        """)
        correlation_data = cursor.fetchall()

        labels = [row['full_name'] for row in correlation_data]
        data = [{'x': row['average_stress'], 'y': row['average_grade'], 'name': row['full_name']} for row in correlation_data]
        
        return {'labels': labels, 'data': data}

    @staticmethod
    def get_dashboard_summary():
        db = get_db()
        total_students = db.execute("SELECT COUNT(id) FROM students WHERE is_active = 1").fetchone()[0]
        total_modules = db.execute("SELECT COUNT(id) FROM modules WHERE is_active = 1").fetchone()[0]
        pending_alerts_count = db.execute("SELECT COUNT(id) FROM alerts WHERE is_active = 1 AND resolved = 0").fetchone()[0]
        total_users = db.execute("SELECT COUNT(id) FROM users WHERE is_active = 1").fetchone()[0]
        
        return {
            'total_students': total_students,
            'total_modules': total_modules,
            'pending_alerts_count': pending_alerts_count,
            'total_users': total_users
        }

    @staticmethod
    def get_overall_attendance_rate():
        db = get_db()
        result = db.execute("SELECT AVG(attendance_rate) FROM attendance_records WHERE is_active = 1").fetchone()[0]
        return round(result * 100, 2) if result is not None else 0

    @staticmethod
    def get_submission_status_distribution():
        db = get_db()
        total_submissions = db.execute("SELECT COUNT(id) FROM submission_records WHERE is_active = 1").fetchone()[0]
        if total_submissions == 0:
            return {'labels': ['Submitted On Time', 'Submitted Late', 'Not Submitted'], 'data': [0, 0, 0]}

        submitted_count = db.execute("SELECT COUNT(id) FROM submission_records WHERE is_active = 1 AND is_submitted = 1 AND is_late = 0").fetchone()[0]
        late_count = db.execute("SELECT COUNT(id) FROM submission_records WHERE is_active = 1 AND is_submitted = 1 AND is_late = 1").fetchone()[0]
        not_submitted_count = db.execute("SELECT COUNT(id) FROM submission_records WHERE is_active = 1 AND is_submitted = 0").fetchone()[0]

        return {
            'labels': ['Submitted On Time', 'Submitted Late', 'Not Submitted'],
            'data': [submitted_count, late_count, not_submitted_count]
        }

    @staticmethod
    def get_high_risk_students(attendance_threshold=70, grade_threshold=40, stress_threshold=4):
        db = get_db()
        high_risk_students = {} # Use dict to store unique students by ID

        # Students with low attendance
        cursor = db.execute(f"""
            SELECT s.id, s.full_name, AVG(ar.attendance_rate) * 100 AS avg_attendance
            FROM students s
            JOIN attendance_records ar ON s.id = ar.student_id
            WHERE s.is_active = 1 AND ar.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING avg_attendance < ?
        """, (attendance_threshold,))
        for row in cursor.fetchall():
            high_risk_students[row['id']] = {'id': row['id'], 'name': row['full_name'], 'reason': f"Low attendance (<{attendance_threshold}%)"}

        # Students with low average grades
        cursor = db.execute(f"""
            SELECT s.id, s.full_name, AVG(g.grade) AS avg_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.is_active = 1 AND g.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING avg_grade < ?
        """, (grade_threshold,))
        for row in cursor.fetchall():
            if row['id'] not in high_risk_students:
                high_risk_students[row['id']] = {'id': row['id'], 'name': row['full_name'], 'reason': f"Low average grade (<{grade_threshold})"}
            else:
                high_risk_students[row['id']]['reason'] += f", Low average grade (<{grade_threshold})"

        # Students with high average stress
        cursor = db.execute(f"""
            SELECT s.id, s.full_name, AVG(sr.stress_level) AS avg_stress
            FROM students s
            JOIN survey_responses sr ON s.id = sr.student_id
            WHERE s.is_active = 1 AND sr.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING avg_stress >= ?
        """, (stress_threshold,))
        for row in cursor.fetchall():
            if row['id'] not in high_risk_students:
                high_risk_students[row['id']] = {'id': row['id'], 'name': row['full_name'], 'reason': f"High average stress (>{stress_threshold-1})"}
            else:
                high_risk_students[row['id']]['reason'] += f", High average stress (>{stress_threshold-1})"
        
        return list(high_risk_students.values())

    @staticmethod
    def get_stress_level_by_module():
        db = get_db()
        cursor = db.execute("""
            SELECT m.module_title, AVG(sr.stress_level) AS average_stress
            FROM modules m
            JOIN survey_responses sr ON m.id = sr.module_id
            WHERE m.is_active = 1 AND sr.is_active = 1
            GROUP BY m.module_title
            ORDER BY average_stress DESC
        """)
        results = cursor.fetchall()
        
        labels = [row['module_title'] for row in results]
        data = [round(row['average_stress'], 2) for row in results]
        return {'labels': labels, 'data': data}
