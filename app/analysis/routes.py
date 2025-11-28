from flask import jsonify
from . import analysis
from app.repositories.student_repository import StudentRepository
from app.repositories.analysis_repository import AnalysisRepository
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required

@analysis.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_students():
    students = StudentRepository.get_all_students()
    return jsonify([{
        'id': student.id,
        'student_number': student.student_number,
        'full_name': student.full_name,
        'email': student.email,
        'course_name': student.course_name,
        'year_of_study': student.year_of_study
    } for student in students])

@analysis.route('/students/<int:student_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_student(student_id):
    student = StudentRepository.get_student_by_id(student_id)
    if student:
        enrolments = StudentRepository.get_student_enrolments(student_id)
        student_dict = student.to_dict()
        student_dict['enrolments'] = [e['module_title'] for e in enrolments]
        return jsonify(student_dict)
    return jsonify({'message': 'Student not found'}), 404

@analysis.route('/students/<int:student_id>/stress-trend', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_trend(student_id):
    """API endpoint for student stress trend."""
    data = AnalysisRepository.get_stress_trend_for_student(student_id)
    return jsonify(data)

@analysis.route('/students/<int:student_id>/attendance-trend', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_attendance_trend(student_id):
    """API endpoint for student attendance trend."""
    data = AnalysisRepository.get_attendance_trend_for_student(student_id)
    return jsonify(data)

@analysis.route('/grade-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_grade_distribution():
    """API endpoint for overall grade distribution."""
    data = AnalysisRepository.get_grade_distribution()
    return jsonify(data)

@analysis.route('/stress-grade-correlation', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_grade_correlation():
    """API endpoint for stress vs. grade correlation."""
    data = AnalysisRepository.get_stress_grade_correlation()
    return jsonify(data)

@analysis.route('/dashboard-summary', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_dashboard_summary():
    """API endpoint for dashboard summary statistics."""
    data = AnalysisRepository.get_dashboard_summary()
    return jsonify(data)

@analysis.route('/overall-attendance-rate', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_overall_attendance_rate():
    """API endpoint for overall average attendance rate."""
    rate = AnalysisRepository.get_overall_attendance_rate()
    return jsonify({'overall_attendance_rate': rate})

@analysis.route('/submission-status-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_submission_status_distribution():
    """API endpoint for submission status distribution."""
    data = AnalysisRepository.get_submission_status_distribution()
    return jsonify(data)

@analysis.route('/high-risk-students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer', 'course_director']) # Added 'course_director'
def get_high_risk_students():
    """API endpoint for high-risk students."""
    students = AnalysisRepository.get_high_risk_students()
    return jsonify(students)

@analysis.route('/stress-by-module', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_by_module():
    """API endpoint for average stress level by module."""
    data = AnalysisRepository.get_stress_level_by_module()
    return jsonify(data)
