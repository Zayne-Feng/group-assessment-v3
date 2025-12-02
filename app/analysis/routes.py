"""
Analysis Blueprint routes for retrieving and visualizing student data insights.

This module defines API endpoints that provide various analytical views
on student wellbeing, academic performance, and engagement. These endpoints
are typically accessed by staff roles (admin, course_director, wellbeing_officer)
to gain insights and identify at-risk students.
"""

from flask import jsonify, current_app # Import current_app for logging
from . import analysis
from app.repositories.student_repository import student_repository
from app.repositories.analysis_repository import analysis_repository
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required

@analysis.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_students():
    """
    Retrieves a list of all students with basic details for analysis purposes.

    Returns:
        Response: JSON array of student objects.
                  - 200 OK: Successfully retrieved student list.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        students = student_repository.get_all_students()
        return jsonify([{
            'id': student.id,
            'student_number': student.student_number,
            'full_name': student.full_name,
            'email': student.email,
            'course_name': student.course_name,
            'year_of_study': student.year_of_study
        } for student in students]), 200
    except Exception as e:
        current_app.logger.error(f"Error getting students for analysis: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/students/<int:student_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_student(student_id):
    """
    Retrieves a single student's details along with their enrolments.

    Args:
        student_id (int): The ID of the student to retrieve.

    Returns:
        Response: JSON object of the student's details and enrolments.
                  - 200 OK: Successfully retrieved student details.
                  - 404 Not Found: Student not found.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        student = student_repository.get_student_by_id(student_id)
        if student:
            enrolments = student_repository.get_student_enrolments(student_id)
            student_dict = student.to_dict()
            student_dict['enrolments'] = [e['module_title'] for e in enrolments]
            return jsonify(student_dict), 200
        return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting student {student_id} for analysis: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/students/<int:student_id>/stress-trend', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_trend(student_id):
    """
    Retrieves the stress level trend for a specific student over weeks.

    Args:
        student_id (int): The ID of the student.

    Returns:
        Response: JSON object containing labels (weeks) and data (average stress levels).
                  - 200 OK: Successfully retrieved stress trend.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_stress_trend_for_student(student_id)
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting stress trend for student {student_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/students/<int:student_id>/attendance-trend', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_attendance_trend(student_id):
    """
    Retrieves the attendance rate trend for a specific student over weeks.

    Args:
        student_id (int): The ID of the student.

    Returns:
        Response: JSON object containing labels (weeks) and data (average attendance rates).
                  - 200 OK: Successfully retrieved attendance trend.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_attendance_trend_for_student(student_id)
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting attendance trend for student {student_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/students/<int:student_id>/average-attendance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_average_attendance_for_student(student_id):
    """
    Retrieves the overall average attendance rate for a specific student.

    Args:
        student_id (int): The ID of the student.

    Returns:
        Response: JSON object with the average attendance rate.
                  - 200 OK: Successfully retrieved average attendance.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        average_attendance = analysis_repository.get_average_attendance_for_student(student_id)
        return jsonify({'average_attendance': average_attendance}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting average attendance for student {student_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/grade-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_grade_distribution():
    """
    Retrieves the distribution of average grades across all students.

    Returns:
        Response: JSON object containing labels (grade bands) and data (number of students).
                  - 200 OK: Successfully retrieved grade distribution.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_grade_distribution()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting grade distribution: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/stress-grade-correlation', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_grade_correlation():
    """
    Retrieves data points for correlating average stress levels with average grades for each student.

    Returns:
        Response: JSON object containing labels (student names) and data (stress-grade data points).
                  - 200 OK: Successfully retrieved correlation data.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_stress_grade_correlation()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting stress-grade correlation: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/dashboard-summary', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_dashboard_summary():
    """
    Retrieves a summary of key metrics for the dashboard, such as total students, modules, and pending alerts.

    Returns:
        Response: JSON object with dashboard summary data.
                  - 200 OK: Successfully retrieved dashboard summary.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_dashboard_summary()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting dashboard summary: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/overall-attendance-rate', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_overall_attendance_rate():
    """
    Retrieves the overall average attendance rate across all students.

    Returns:
        Response: JSON object with the overall attendance rate.
                  - 200 OK: Successfully retrieved overall attendance rate.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        rate = analysis_repository.get_overall_attendance_rate()
        return jsonify({'overall_attendance_rate': rate}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting overall attendance rate: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/submission-status-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_submission_status_distribution():
    """
    Retrieves the distribution of submission statuses (e.g., on time, late, not submitted).

    Returns:
        Response: JSON object containing labels and data for the distribution.
                  - 200 OK: Successfully retrieved submission status distribution.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_submission_status_distribution()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting submission status distribution: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/high-risk-students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer', 'course_director'])
def get_high_risk_students():
    """
    Identifies and retrieves a list of students who are considered high-risk
    based on predefined thresholds for attendance, grades, and stress levels.

    Returns:
        Response: JSON array of high-risk student objects with reasons.
                  - 200 OK: Successfully retrieved high-risk students.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        students = analysis_repository.get_high_risk_students()
        return jsonify(students), 200
    except Exception as e:
        current_app.logger.error(f"Error getting high-risk students: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@analysis.route('/stress-by-module', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_by_module():
    """
    Retrieves the average stress level aggregated by module.

    Returns:
        Response: JSON object containing labels (module titles) and data (average stress levels).
                  - 200 OK: Successfully retrieved stress by module data.
                  - 500 Internal Server Error: An unexpected error occurred.
    """
    try:
        data = analysis_repository.get_stress_level_by_module()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting stress by module: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500
