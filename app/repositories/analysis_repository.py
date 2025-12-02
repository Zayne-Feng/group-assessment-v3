"""
Analysis Repository module for complex data analysis queries.

This module defines the `AnalysisRepository` class, which provides methods
for performing various analytical queries on student data. It extends
`BaseRepository` but primarily focuses on custom SQL queries to extract
insights related to student wellbeing, academic performance, and engagement.
"""

import sqlite3
from app.db_connection import get_db
from app.models.survey_response import SurveyResponse
from app.models.attendance_record import AttendanceRecord
from app.models.grade import Grade
from app.models.student import Student
from app.models.module import Module
from app.models.alert import Alert
from app.models.submission_record import SubmissionRecord
from datetime import datetime
from .base_repository import BaseRepository

class AnalysisRepository(BaseRepository):
    """
    Repository for complex data analysis queries.

    Inherits from `BaseRepository` to utilize its underlying database
    connection and error handling mechanisms. This repository focuses
    on aggregating and transforming raw data into meaningful insights
    for the Student Wellbeing Monitoring System.
    """
    def __init__(self):
        """
        Initializes the AnalysisRepository.

        Sets the table name to 'analysis' (a conceptual table as it performs
        cross-table queries) and `model_class` to None, as results are typically
        returned as aggregated dictionaries.
        """
        super().__init__('analysis', None) 

    def get_stress_trend_for_student(self, student_id: int) -> dict:
        """
        Retrieves the stress level trend for a specific student over academic weeks.

        Aggregates average stress levels from survey responses per week.

        Args:
            student_id (int): The unique identifier of the student.

        Returns:
            dict: A dictionary containing two lists:
                  - 'labels': List of week numbers (e.g., "Week 1", "Week 2").
                  - 'data': List of average stress levels for each corresponding week.
        """
        query = """
            SELECT week_number, AVG(stress_level) as average_stress_level FROM survey_responses
            WHERE student_id = ? AND is_active = 1
            GROUP BY week_number
            ORDER BY week_number
        """
        records = self._execute_query(query, (student_id,), fetch_all_dicts=True)
        
        return {
            'labels': [f"Week {row['week_number']}" for row in records],
            'data': [round(row['average_stress_level'], 2) for row in records]
        }

    def get_attendance_trend_for_student(self, student_id: int) -> dict:
        """
        Retrieves the attendance rate trend for a specific student over academic weeks.

        Aggregates average attendance rates from attendance records per week.

        Args:
            student_id (int): The unique identifier of the student.

        Returns:
            dict: A dictionary containing two lists:
                  - 'labels': List of week numbers (e.g., "Week 1", "Week 2").
                  - 'data': List of average attendance rates (as percentages) for each corresponding week.
        """
        query = """
            SELECT week_number, AVG(attendance_rate) as average_attendance_rate FROM attendance_records
            WHERE student_id = ? AND is_active = 1
            GROUP BY week_number
            ORDER BY week_number
        """
        records = self._execute_query(query, (student_id,), fetch_all_dicts=True)
        
        return {
            'labels': [f"Week {row['week_number']}" for row in records],
            'data': [round(row['average_attendance_rate'] * 100, 2) if row['average_attendance_rate'] is not None else 0 for row in records]
        }

    def get_average_attendance_for_student(self, student_id: int) -> float:
        """
        Calculates the overall average attendance rate for a specific student across all modules.

        Args:
            student_id (int): The unique identifier of the student.

        Returns:
            float: The overall average attendance rate for the student, as a percentage (0-100).
                   Returns 0 if no attendance records are found.
        """
        query = """
            SELECT AVG(attendance_rate) AS overall_average_attendance
            FROM attendance_records
            WHERE student_id = ? AND is_active = 1
        """
        result = self._execute_query(query, (student_id,), fetch_one=True)
        return round(result * 100, 2) if result is not None else 0

    def get_grade_distribution(self) -> dict:
        """
        Calculates the distribution of average grades across all active students.

        Students are categorized into predefined grade bands (Fail, Pass, Merit, etc.).

        Returns:
            dict: A dictionary containing two lists:
                  - 'labels': List of grade band names (e.g., "Fail (<40)", "Pass (40-49)").
                  - 'data': List of the count of students falling into each grade band.
        """
        grade_bands = {
            'Fail (<40)': 0, 'Pass (40-49)': 0, 'Merit (50-59)': 0,
            'Distinction (60-69)': 0, 'Excellent (70+)': 0
        }
        
        query = """
            SELECT s.id, AVG(g.grade) AS average_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.is_active = 1 AND g.is_active = 1
            GROUP BY s.id
        """
        avg_grades = self._execute_query(query, fetch_all_dicts=True)

        for row in avg_grades:
            avg_grade = row['average_grade']
            if avg_grade is None: continue # Skip students with no grades.
            if avg_grade < 40: grade_bands['Fail (<40)'] += 1
            elif 40 <= avg_grade < 50: grade_bands['Pass (40-49)'] += 1
            elif 50 <= avg_grade < 60: grade_bands['Merit (50-59)'] += 1
            elif 60 <= avg_grade < 70: grade_bands['Distinction (60-69)'] += 1
            else: grade_bands['Excellent (70+)'] += 1
        
        return {'labels': list(grade_bands.keys()), 'data': list(grade_bands.values())}

    def get_stress_grade_correlation(self) -> dict:
        """
        Retrieves data for correlating average stress levels with average grades for each student.

        This data can be used to plot scatter charts to visualize potential relationships.

        Returns:
            dict: A dictionary containing:
                  - 'labels': List of student full names.
                  - 'data': List of dictionaries, each representing a data point with 'x' (average stress),
                            'y' (average grade), and 'name' (student full name).
        """
        query = """
            SELECT s.full_name, AVG(sr.stress_level) AS average_stress, AVG(g.grade) AS average_grade
            FROM students s
            LEFT JOIN survey_responses sr ON s.id = sr.student_id AND sr.is_active = 1
            LEFT JOIN grades g ON s.id = g.student_id AND g.is_active = 1
            WHERE s.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING average_stress IS NOT NULL AND average_grade IS NOT NULL
        """
        correlation_data = self._execute_query(query, fetch_all_dicts=True)

        labels = [row['full_name'] for row in correlation_data]
        data = [{'x': row['average_stress'], 'y': row['average_grade'], 'name': row['full_name']} for row in correlation_data]
        
        return {'labels': labels, 'data': data}

    def get_dashboard_summary(self) -> dict:
        """
        Retrieves a summary of key metrics for the application dashboard.

        Includes counts for total active students, modules, pending alerts, and active users.

        Returns:
            dict: A dictionary containing the summarized metrics.
        """
        total_students = self._execute_query("SELECT COUNT(id) AS count FROM students WHERE is_active = 1", fetch_one=True)
        total_modules = self._execute_query("SELECT COUNT(id) AS count FROM modules WHERE is_active = 1", fetch_one=True)
        pending_alerts_count = self._execute_query("SELECT COUNT(id) AS count FROM alerts WHERE is_active = 1 AND resolved = 0", fetch_one=True)
        total_users = self._execute_query("SELECT COUNT(id) AS count FROM users WHERE is_active = 1", fetch_one=True)
        
        return {
            'total_students': total_students if total_students is not None else 0,
            'total_modules': total_modules if total_modules is not None else 0,
            'pending_alerts_count': pending_alerts_count if pending_alerts_count is not None else 0,
            'total_users': total_users if total_users is not None else 0
        }

    def get_overall_attendance_rate(self) -> float:
        """
        Calculates the overall average attendance rate across all active students and modules.

        Returns:
            float: The overall average attendance rate, as a percentage (0-100).
                   Returns 0 if no attendance records are found.
        """
        result = self._execute_query("SELECT AVG(attendance_rate) AS avg_rate FROM attendance_records WHERE is_active = 1", fetch_one=True)
        return round(result * 100, 2) if result is not None else 0

    def get_submission_status_distribution(self) -> dict:
        """
        Calculates the distribution of assessment submission statuses (on time, late, not submitted).

        Returns:
            dict: A dictionary containing:
                  - 'labels': List of submission status categories.
                  - 'data': List of counts for each submission status.
        """
        total_submissions = self._execute_query("SELECT COUNT(id) AS count FROM submission_records WHERE is_active = 1", fetch_one=True)
        if total_submissions == 0:
            return {'labels': ['Submitted On Time', 'Submitted Late', 'Not Submitted'], 'data': [0, 0, 0]}

        submitted_count = self._execute_query("SELECT COUNT(id) AS count FROM submission_records WHERE is_active = 1 AND is_submitted = 1 AND is_late = 0", fetch_one=True)
        late_count = self._execute_query("SELECT COUNT(id) AS count FROM submission_records WHERE is_active = 1 AND is_submitted = 1 AND is_late = 1", fetch_one=True)
        not_submitted_count = self._execute_query("SELECT COUNT(id) AS count FROM submission_records WHERE is_active = 1 AND is_submitted = 0", fetch_one=True)

        return {
            'labels': ['Submitted On Time', 'Submitted Late', 'Not Submitted'],
            'data': [submitted_count if submitted_count is not None else 0, 
                     late_count if late_count is not None else 0, 
                     not_submitted_count if not_submitted_count is not None else 0]
        }

    def get_high_risk_students(self, attendance_threshold: int = 70, grade_threshold: int = 40, stress_threshold: int = 4) -> list[dict]:
        """
        Identifies high-risk students based on configurable thresholds for attendance, grades, and stress levels.

        Args:
            attendance_threshold (int, optional): The attendance percentage below which a student is considered at risk. Defaults to 70.
            grade_threshold (int, optional): The average grade below which a student is considered at risk. Defaults to 40.
            stress_threshold (int, optional): The average stress level (1-5) above which a student is considered at risk. Defaults to 4.

        Returns:
            list[dict]: A list of dictionaries, each representing a high-risk student
                        and a concatenated string of reasons for their risk status.
        """
        high_risk_students = {}

        # Query for students with low attendance.
        query_low_attendance = f"""
            SELECT s.id, s.full_name, AVG(ar.attendance_rate) * 100 AS avg_attendance
            FROM students s
            JOIN attendance_records ar ON s.id = ar.student_id
            WHERE s.is_active = 1 AND ar.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING avg_attendance < ?
        """
        for row in self._execute_query(query_low_attendance, (attendance_threshold,), fetch_all_dicts=True):
            high_risk_students[row['id']] = {'id': row['id'], 'name': row['full_name'], 'reason': f"Low attendance (<{attendance_threshold}%)"}

        # Query for students with low grades.
        query_low_grades = f"""
            SELECT s.id, s.full_name, AVG(g.grade) AS avg_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.is_active = 1 AND g.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING avg_grade < ?
        """
        for row in self._execute_query(query_low_grades, (grade_threshold,), fetch_all_dicts=True):
            if row['id'] not in high_risk_students:
                high_risk_students[row['id']] = {'id': row['id'], 'name': row['full_name'], 'reason': f"Low average grade (<{grade_threshold})"}
            else:
                high_risk_students[row['id']]['reason'] += f", Low average grade (<{grade_threshold})"

        # Query for students with high stress levels.
        query_high_stress = f"""
            SELECT s.id, s.full_name, AVG(sr.stress_level) AS avg_stress
            FROM students s
            JOIN survey_responses sr ON s.id = sr.student_id
            WHERE s.is_active = 1 AND sr.is_active = 1
            GROUP BY s.id, s.full_name
            HAVING avg_stress >= ?
        """
        for row in self._execute_query(query_high_stress, (stress_threshold,), fetch_all_dicts=True):
            if row['id'] not in high_risk_students:
                high_risk_students[row['id']] = {'id': row['id'], 'name': row['full_name'], 'reason': f"High average stress (>{stress_threshold-1})"}
            else:
                high_risk_students[row['id']]['reason'] += f", High average stress (>{stress_threshold-1})"
        
        return list(high_risk_students.values())

    def get_stress_level_by_module(self) -> dict:
        """
        Calculates the average stress level for each active module.

        Returns:
            dict: A dictionary containing two lists:
                  - 'labels': List of module titles.
                  - 'data': List of average stress levels for each corresponding module.
        """
        query = """
            SELECT m.module_title, AVG(sr.stress_level) AS average_stress
            FROM modules m
            JOIN survey_responses sr ON m.id = sr.module_id
            WHERE m.is_active = 1 AND sr.is_active = 1
            GROUP BY m.module_title
            ORDER BY average_stress DESC
        """
        results = self._execute_query(query, fetch_all_dicts=True)
        
        labels = [row['module_title'] for row in results]
        data = [round(row['average_stress'], 2) for row in results]
        return {'labels': labels, 'data': data}

# Instantiate the repository for use throughout the application.
analysis_repository = AnalysisRepository()
