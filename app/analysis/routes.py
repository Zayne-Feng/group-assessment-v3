from flask import jsonify
from . import analysis
from app.repositories.student_repository import student_repository
from app.repositories.analysis_repository import analysis_repository
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required

@analysis.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_students():
    students = student_repository.get_all_students()
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
    student = student_repository.get_student_by_id(student_id)
    if student:
        enrolments = student_repository.get_student_enrolments(student_id)
        student_dict = student.to_dict()
        student_dict['enrolments'] = [e['module_title'] for e in enrolments]
        return jsonify(student_dict)
    return jsonify({'message': 'Student not found'}), 404

@analysis.route('/students/<int:student_id>/stress-trend', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_trend(student_id):
    data = analysis_repository.get_stress_trend_for_student(student_id)
    return jsonify(data)

@analysis.route('/students/<int:student_id>/attendance-trend', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_attendance_trend(student_id):
    data = analysis_repository.get_attendance_trend_for_student(student_id)
    return jsonify(data)

@analysis.route('/students/<int:student_id>/average-attendance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_average_attendance_for_student(student_id):
    average_attendance = analysis_repository.get_average_attendance_for_student(student_id)
    return jsonify({'average_attendance': average_attendance})

@analysis.route('/grade-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_grade_distribution():
    data = analysis_repository.get_grade_distribution()
    return jsonify(data)

@analysis.route('/stress-grade-correlation', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_grade_correlation():
    data = analysis_repository.get_stress_grade_correlation()
    return jsonify(data)

@analysis.route('/dashboard-summary', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_dashboard_summary():
    data = analysis_repository.get_dashboard_summary()
    return jsonify(data)

@analysis.route('/overall-attendance-rate', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_overall_attendance_rate():
    rate = analysis_repository.get_overall_attendance_rate()
    return jsonify({'overall_attendance_rate': rate})

@analysis.route('/submission-status-distribution', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_submission_status_distribution():
    data = analysis_repository.get_submission_status_distribution()
    return jsonify(data)

@analysis.route('/high-risk-students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer', 'course_director'])
def get_high_risk_students():
    students = analysis_repository.get_high_risk_students()
    return jsonify(students)

@analysis.route('/stress-by-module', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_stress_by_module():
    data = analysis_repository.get_stress_level_by_module()
    return jsonify(data)
