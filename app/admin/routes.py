from flask import request, jsonify
from . import admin
from app.repositories.module_repository import module_repository
from app.repositories.alert_repository import alert_repository
from app.repositories.student_repository import student_repository
from app.repositories.user_repository import user_repository
from app.repositories.survey_response_repository import survey_response_repository
from app.repositories.enrolment_repository import enrolment_repository
from app.repositories.attendance_record_repository import attendance_record_repository
from app.repositories.submission_record_repository import submission_record_repository
from app.repositories.grade_repository import grade_repository
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required

# region Module Endpoints
@admin.route('/modules', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director'])
def get_modules():
    modules = module_repository.get_all_modules()
    return jsonify([module.to_dict() for module in modules])

@admin.route('/modules', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_module():
    data = request.get_json()
    module = module_repository.create_module(data.get('module_code'), data.get('module_title'), data.get('credit'), data.get('academic_year'))
    if module:
        return jsonify({'message': 'Module created successfully', 'id': module.id}), 201
    return jsonify({'message': 'Failed to create module'}), 400

@admin.route('/modules/<int:module_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director'])
def get_module(module_id):
    module = module_repository.get_module_by_id(module_id)
    if module:
        return jsonify(module.to_dict())
    return jsonify({'message': 'Module not found'}), 404

@admin.route('/modules/<int:module_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_module(module_id):
    data = request.get_json()
    module = module_repository.update_module(module_id, data.get('module_code'), data.get('module_title'), data.get('credit'), data.get('academic_year'))
    if module:
        return jsonify({'message': 'Module updated successfully'}), 200
    return jsonify({'message': 'Module not found or failed to update'}), 404

@admin.route('/modules/<int:module_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_module(module_id):
    if module_repository.delete_module(module_id):
        return jsonify({'message': 'Module deleted successfully'}), 200
    return jsonify({'message': 'Module not found or failed to delete'}), 404
# endregion

# region Alert Endpoints
@admin.route('/alerts', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def get_alerts():
    alerts_data = alert_repository.get_recent_alerts_per_student()
    return jsonify(alerts_data)

@admin.route('/alerts/student/<int:student_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer', 'course_director'])
def get_alerts_for_student(student_id):
    alerts_data = alert_repository.get_alerts_by_student_id(student_id)
    return jsonify(alerts_data)

@admin.route('/alerts/<int:alert_id>/resolve', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def resolve_alert(alert_id):
    if alert_repository.mark_alert_resolved(alert_id):
        return jsonify({'message': 'Alert marked as resolved'}), 200
    return jsonify({'message': 'Alert not found or failed to resolve'}), 404

@admin.route('/alerts/<int:alert_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def delete_alert_logical(alert_id):
    if alert_repository.delete_alert(alert_id):
        return jsonify({'message': 'Alert deleted successfully'}), 200
    return jsonify({'message': 'Alert not found or failed to delete'}), 404
# endregion

# region Student Endpoints
@admin.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director', 'wellbeing_officer'])
def get_students():
    students = student_repository.get_all_students()
    return jsonify([s.to_dict() for s in students])

@admin.route('/students', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_student():
    data = request.get_json()
    student = student_repository.create_student(data.get('student_number'), data.get('full_name'), data.get('email'), data.get('course_name'), data.get('year_of_study'))
    if student:
        return jsonify({'message': 'Student created successfully', 'id': student.id}), 201
    return jsonify({'message': 'Failed to create student'}), 400

@admin.route('/students/<int:student_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_student(student_id):
    data = request.get_json()
    student = student_repository.update_student(student_id, data.get('student_number'), data.get('full_name'), data.get('email'), data.get('course_name'), data.get('year_of_study'))
    if student:
        return jsonify({'message': 'Student updated successfully'}), 200
    return jsonify({'message': 'Student not found or failed to update'}), 404

@admin.route('/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_student(student_id):
    if student_repository.delete_student(student_id):
        return jsonify({'message': 'Student deleted successfully'}), 200
    return jsonify({'message': 'Student not found or failed to delete'}), 404
# endregion

# region User Endpoints
@admin.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = user_repository.get_all_users()
    return jsonify([user.to_dict() for user in users])

@admin.route('/users', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    data = request.get_json()
    user = user_repository.create_user(data.get('username'), data.get('password'), data.get('role'))
    if user:
        return jsonify({'message': 'User created successfully', 'id': user.id}), 201
    return jsonify({'message': 'Failed to create user'}), 400

@admin.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_user(user_id):
    user = user_repository.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404

@admin.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(user_id):
    data = request.get_json()
    user = user_repository.update_user(user_id, data.get('username'), data.get('role'), data.get('is_active'))
    if user:
        return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'message': 'User not found or failed to update'}), 404

@admin.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    if user_repository.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found or failed to delete'}), 404

@admin.route('/users/<int:user_id>/reset-password', methods=['PUT'])
@jwt_required()
@role_required('admin')
def reset_user_password(user_id):
    data = request.get_json()
    new_password = data.get('new_password')
    if not new_password:
        return jsonify({'message': 'New password is required'}), 400
    if user_repository.reset_password(user_id, new_password):
        return jsonify({'message': 'User password reset successfully'}), 200
    return jsonify({'message': 'User not found or failed to reset password'}), 404
# endregion

# region Survey Response Endpoints
@admin.route('/survey-responses', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def get_survey_responses():
    surveys = survey_response_repository.get_all_survey_responses()
    return jsonify(surveys)

@admin.route('/survey-responses', methods=['POST'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer', 'user', 'student'])
def create_survey_response():
    data = request.get_json()
    survey = survey_response_repository.create_survey_response(data.get('student_id'), data.get('module_id'), data.get('week_number'), data.get('stress_level'), data.get('hours_slept'), data.get('mood_comment'))
    if survey:
        return jsonify({'message': 'Survey response created successfully', 'id': survey.id}), 201
    return jsonify({'message': 'Failed to create survey response'}), 400

@admin.route('/survey-responses/<int:response_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def update_survey_response(response_id):
    data = request.get_json()
    survey = survey_response_repository.update_survey_response(response_id, data.get('student_id'), data.get('module_id'), data.get('week_number'), data.get('stress_level'), data.get('hours_slept'), data.get('mood_comment'))
    if survey:
        return jsonify({'message': 'Survey response updated successfully'}), 200
    return jsonify({'message': 'Survey response not found or failed to update'}), 404

@admin.route('/survey-responses/<int:response_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def delete_survey_response(response_id):
    if survey_response_repository.delete_survey_response(response_id):
        return jsonify({'message': 'Survey response deleted successfully'}), 200
    return jsonify({'message': 'Survey response not found or failed to delete'}), 404
# endregion

# region Enrolment Endpoints
@admin.route('/enrolments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director'])
def get_enrolments():
    enrolments_data = enrolment_repository.get_all_enrolments()
    return jsonify(enrolments_data)

@admin.route('/enrolments', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_enrolment():
    data = request.get_json()
    enrolment = enrolment_repository.create_enrolment(data.get('student_id'), data.get('module_id'), data.get('enrol_date'))
    if enrolment:
        return jsonify({'message': 'Enrolment created successfully', 'id': enrolment.id}), 201
    return jsonify({'message': 'Failed to create enrolment'}), 400

@admin.route('/enrolments/<int:enrolment_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_enrolment(enrolment_id):
    data = request.get_json()
    enrolment = enrolment_repository.update_enrolment(enrolment_id, data.get('student_id'), data.get('module_id'), data.get('enrol_date'))
    if enrolment:
        return jsonify({'message': 'Enrolment updated successfully'}), 200
    return jsonify({'message': 'Enrolment not found or failed to update'}), 404

@admin.route('/enrolments/<int:enrolment_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_enrolment(enrolment_id):
    if enrolment_repository.delete_enrolment(enrolment_id):
        return jsonify({'message': 'Enrolment deleted successfully'}), 200
    return jsonify({'message': 'Enrolment not found or failed to delete'}), 404
# endregion

# region Attendance Record Endpoints
@admin.route('/attendance-records', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director'])
def get_attendance_records():
    records_data = attendance_record_repository.get_all_attendance_records()
    return jsonify(records_data)

@admin.route('/attendance-records', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_attendance_record():
    data = request.get_json()
    record = attendance_record_repository.create_attendance_record(data.get('student_id'), data.get('module_id'), data.get('week_number'), data.get('attended_sessions'), data.get('total_sessions'))
    if record:
        return jsonify({'message': 'Attendance record created successfully', 'id': record.id}), 201
    return jsonify({'message': 'Failed to create attendance record'}), 400

@admin.route('/attendance-records/<int:record_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_attendance_record(record_id):
    data = request.get_json()
    record = attendance_record_repository.update_attendance_record(record_id, data.get('student_id'), data.get('module_id'), data.get('week_number'), data.get('attended_sessions'), data.get('total_sessions'))
    if record:
        return jsonify({'message': 'Attendance record updated successfully'}), 200
    return jsonify({'message': 'Attendance record not found or failed to update'}), 404

@admin.route('/attendance-records/<int:record_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_attendance_record(record_id):
    if attendance_record_repository.delete_attendance_record(record_id):
        return jsonify({'message': 'Attendance record deleted successfully'}), 200
    return jsonify({'message': 'Attendance record not found or failed to delete'}), 404
# endregion

# region Submission Record Endpoints
@admin.route('/submission-records', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director'])
def get_submission_records():
    records_data = submission_record_repository.get_all_submission_records()
    return jsonify(records_data)

@admin.route('/submission-records', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_submission_record():
    data = request.get_json()
    record = submission_record_repository.create_submission_record(data.get('student_id'), data.get('module_id'), data.get('assessment_name'), data.get('due_date'), data.get('submitted_date'), data.get('is_submitted'), data.get('is_late'))
    if record:
        return jsonify({'message': 'Submission record created successfully', 'id': record.id}), 201
    return jsonify({'message': 'Failed to create submission record'}), 400

@admin.route('/submission-records/<int:record_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_submission_record(record_id):
    data = request.get_json()
    record = submission_record_repository.update_submission_record(record_id, data.get('student_id'), data.get('module_id'), data.get('assessment_name'), data.get('due_date'), data.get('submitted_date'), data.get('is_submitted'), data.get('is_late'))
    if record:
        return jsonify({'message': 'Submission record updated successfully'}), 200
    return jsonify({'message': 'Submission record not found or failed to update'}), 404

@admin.route('/submission-records/<int:record_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_submission_record(record_id):
    if submission_record_repository.delete_submission_record(record_id):
        return jsonify({'message': 'Submission record deleted successfully'}), 200
    return jsonify({'message': 'Submission record not found or failed to delete'}), 404
# endregion

# region Grade Endpoints
@admin.route('/grades', methods=['GET'])
@jwt_required()
@role_required(['admin', 'course_director'])
def get_grades():
    grades_data = grade_repository.get_all_grades()
    return jsonify(grades_data)

@admin.route('/grades', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_grade():
    data = request.get_json()
    grade = grade_repository.create_grade(data.get('student_id'), data.get('module_id'), data.get('assessment_name'), data.get('grade'))
    if grade:
        return jsonify({'message': 'Grade created successfully', 'id': grade.id}), 201
    return jsonify({'message': 'Failed to create grade'}), 400

@admin.route('/grades/<int:grade_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_grade(grade_id):
    data = request.get_json()
    grade = grade_repository.update_grade(grade_id, data.get('student_id'), data.get('module_id'), data.get('assessment_name'), data.get('grade'))
    if grade:
        return jsonify({'message': 'Grade updated successfully'}), 200
    return jsonify({'message': 'Grade not found or failed to update'}), 404

@admin.route('/grades/<int:grade_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_grade(grade_id):
    if grade_repository.delete_grade(grade_id):
        return jsonify({'message': 'Grade deleted successfully'}), 200
    return jsonify({'message': 'Grade not found or failed to delete'}), 404
# endregion
