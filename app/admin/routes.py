"""
Admin Blueprint routes for managing application data.

This module defines API endpoints accessible by administrators (and sometimes other staff roles)
to perform CRUD (Create, Read, Update, Delete) operations on various data entities
within the Student Wellbeing Monitoring System. It includes specific routes for
Modules, Alerts, Students, Users, and a generic CRUD mechanism for other entities.
"""

from flask import request, jsonify, current_app
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
@admin.route('/modules', methods=['GET', 'POST'])
@jwt_required()
def handle_modules():
    """
    Handles requests for the /modules endpoint.
    - GET: Retrieves all modules.
    - POST: Creates a new module.
    Requires 'admin' or 'course_director' role for GET, 'admin' for POST.
    """
    if request.method == 'GET':
        @role_required(['admin', 'course_director'])
        def get_all_modules():
            """Retrieves all modules."""
            try:
                modules = module_repository.get_all_modules()
                return jsonify([module.to_dict() for module in modules]), 200
            except Exception as e:
                current_app.logger.error(f"Error getting all modules: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return get_all_modules()
    
    elif request.method == 'POST':
        @role_required('admin')
        def create_module():
            """Creates a new module."""
            data = request.get_json()
            # Validate required fields for module creation.
            if not data or not all(k in data for k in ['module_code', 'module_title']):
                return jsonify({'message': 'Missing required fields: module_code, module_title.'}), 400
            try:
                module = module_repository.create_module(**data)
                return jsonify({'message': 'Module created successfully', 'id': module.id}), 201
            except Exception as e:
                current_app.logger.error(f"Error creating module: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return create_module()

@admin.route('/modules/<int:module_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_module(module_id):
    """
    Handles requests for a specific module by ID.
    - GET: Retrieves a single module.
    - PUT: Updates an existing module.
    - DELETE: Logically deletes a module.
    Requires 'admin' or 'course_director' role for GET, 'admin' for PUT/DELETE.

    Args:
        module_id (int): The ID of the module to operate on.
    """
    if request.method == 'GET':
        @role_required(['admin', 'course_director'])
        def get_single_module(module_id):
            """Retrieves a single module by ID."""
            try:
                module = module_repository.get_module_by_id(module_id)
                if module:
                    return jsonify(module.to_dict()), 200
                return jsonify({'message': 'Module not found'}), 404
            except Exception as e:
                current_app.logger.error(f"Error getting module {module_id}: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return get_single_module(module_id)

    elif request.method == 'PUT':
        @role_required('admin')
        def update_single_module(module_id):
            """Updates an existing module by ID."""
            data = request.get_json()
            if not data: return jsonify({'message': 'Request body is empty.'}), 400
            try:
                existing = module_repository.get_module_by_id(module_id)
                if not existing: return jsonify({'message': 'Module not found'}), 404
                
                # Merge existing data with new data.
                update_data = existing.to_dict()
                update_data.update(data)
                
                # Remove fields that are not expected by the repository's update method.
                update_data.pop('id', None)
                update_data.pop('is_active', None)
                update_data.pop('created_at', None) 

                updated = module_repository.update_module(module_id, **update_data)
                return jsonify({'message': 'Module updated successfully'}), 200
            except Exception as e:
                current_app.logger.error(f"Error updating module {module_id}: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return update_single_module(module_id)

    elif request.method == 'DELETE':
        @role_required('admin')
        def delete_single_module(module_id):
            """Logically deletes a module by ID."""
            try:
                if module_repository.delete_module(module_id):
                    return jsonify({'message': 'Module deleted successfully'}), 200
                return jsonify({'message': 'Module not found'}), 404
            except Exception as e:
                current_app.logger.error(f"Error deleting module {module_id}: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return delete_single_module(module_id)
# endregion

# region Alert Endpoints
@admin.route('/alerts', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def get_alerts():
    """
    Retrieves a list of recent alerts.
    Requires 'admin' or 'wellbeing_officer' role.
    """
    try:
        alerts_data = alert_repository.get_recent_alerts_per_student()
        return jsonify(alerts_data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting alerts: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@admin.route('/alerts/student/<int:student_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer', 'course_director'])
def get_alerts_for_student(student_id):
    """
    Retrieves alerts specific to a student.
    Requires 'admin', 'wellbeing_officer', or 'course_director' role.

    Args:
        student_id (int): The ID of the student.
    """
    try:
        alerts_data = alert_repository.get_alerts_by_student_id(student_id)
        return jsonify(alerts_data), 200
    except Exception as e:
        current_app.logger.error(f"Error getting alerts for student {student_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@admin.route('/alerts/<int:alert_id>/resolve', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def resolve_alert(alert_id):
    """
    Marks a specific alert as resolved.
    Requires 'admin' or 'wellbeing_officer' role.

    Args:
        alert_id (int): The ID of the alert to resolve.
    """
    try:
        if alert_repository.mark_alert_resolved(alert_id):
            return jsonify({'message': 'Alert marked as resolved'}), 200
        return jsonify({'message': 'Alert not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error resolving alert {alert_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@admin.route('/alerts/<int:alert_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'wellbeing_officer'])
def delete_alert_logical(alert_id):
    """
    Logically deletes a specific alert.
    Requires 'admin' or 'wellbeing_officer' role.

    Args:
        alert_id (int): The ID of the alert to logically delete.
    """
    try:
        if alert_repository.delete_alert(alert_id):
            return jsonify({'message': 'Alert deleted successfully'}), 200
        return jsonify({'message': 'Alert not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error deleting alert {alert_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500
# endregion

# region Student Endpoints
@admin.route('/students', methods=['GET', 'POST'])
@jwt_required()
def handle_students():
    """
    Handles requests for the /students endpoint.
    - GET: Retrieves all students.
    - POST: Creates a new student.
    Requires 'admin', 'course_director', or 'wellbeing_officer' role for GET, 'admin' for POST.
    """
    if request.method == 'GET':
        @role_required(['admin', 'course_director', 'wellbeing_officer'])
        def get_all_students():
            """Retrieves all students."""
            try:
                students = student_repository.get_all_students()
                return jsonify([s.to_dict() for s in students]), 200
            except Exception as e:
                current_app.logger.error(f"Error getting all students: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return get_all_students()

    elif request.method == 'POST':
        @role_required('admin')
        def create_student():
            """Creates a new student."""
            data = request.get_json()
            if not data or not all(k in data for k in ['student_number', 'full_name']):
                return jsonify({'message': 'Missing required fields: student_number, full_name.'}), 400
            try:
                student = student_repository.create_student(**data)
                return jsonify({'message': 'Student created successfully', 'id': student.id}), 201
            except Exception as e:
                current_app.logger.error(f"Error creating student: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return create_student()

@admin.route('/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_student(student_id):
    """
    Handles requests for a specific student by ID.
    - GET: Retrieves a single student.
    - PUT: Updates an existing student.
    - DELETE: Logically deletes a student.
    Requires 'admin', 'course_director', or 'wellbeing_officer' role for GET, 'admin' for PUT/DELETE.

    Args:
        student_id (int): The ID of the student to operate on.
    """
    if request.method == 'GET':
        @role_required(['admin', 'course_director', 'wellbeing_officer'])
        def get_single_student(student_id):
            """Retrieves a single student by ID."""
            try:
                student = student_repository.get_student_by_id(student_id)
                if student: return jsonify(student.to_dict()), 200
                return jsonify({'message': 'Student not found'}), 404
            except Exception as e:
                current_app.logger.error(f"Error getting student {student_id}: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return get_single_student(student_id)

    elif request.method == 'PUT':
        @role_required('admin')
        def update_single_student(student_id):
            """Updates an existing student by ID."""
            data = request.get_json()
            if not data: return jsonify({'message': 'Request body is empty.'}), 400
            try:
                existing = student_repository.get_student_by_id(student_id)
                if not existing: return jsonify({'message': 'Student not found'}), 404
                
                # Merge existing data with new data.
                update_data = existing.to_dict()
                update_data.update(data)

                # Remove fields that are not expected by the repository's update method.
                update_data.pop('id', None)
                update_data.pop('is_active', None)
                update_data.pop('created_at', None) 
                
                updated = student_repository.update_student(student_id, **update_data)
                return jsonify({'message': 'Student updated successfully'}), 200
            except Exception as e:
                current_app.logger.error(f"Error updating student {student_id}: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return update_single_student(student_id)

    elif request.method == 'DELETE':
        @role_required('admin')
        def delete_single_student(student_id):
            """Logically deletes a student by ID."""
            try:
                if student_repository.delete_student(student_id):
                    return jsonify({'message': 'Student deleted successfully'}), 200
                return jsonify({'message': 'Student not found'}), 404
            except Exception as e:
                current_app.logger.error(f"Error deleting student {student_id}: {e}", exc_info=True)
                return jsonify({'message': 'An unexpected error occurred.'}), 500
        return delete_single_student(student_id)
# endregion

# region User Endpoints
@admin.route('/users', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def handle_users():
    """
    Handles requests for the /users endpoint.
    - GET: Retrieves all users.
    - POST: Creates a new user.
    Requires 'admin' role.
    """
    if request.method == 'GET':
        try:
            users = user_repository.get_all_users()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            current_app.logger.error(f"Error getting all users: {e}", exc_info=True)
            return jsonify({'message': 'An unexpected error occurred.'}), 500
    
    elif request.method == 'POST':
        data = request.get_json()
        # Validate required fields for user creation.
        if not data or not all(k in data for k in ['username', 'password', 'role']):
            return jsonify({'message': 'Missing required fields: username, password, role.'}), 400
        try:
            user = user_repository.create_user(**data)
            return jsonify({'message': 'User created successfully', 'id': user.id}), 201
        except Exception as e:
            current_app.logger.error(f"Error creating user: {e}", exc_info=True)
            return jsonify({'message': 'An unexpected error occurred.'}), 500

@admin.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@role_required('admin')
def handle_user(user_id):
    """
    Handles requests for a specific user by ID.
    - GET: Retrieves a single user.
    - PUT: Updates an existing user.
    - DELETE: Logically deletes a user.
    Requires 'admin' role.

    Args:
        user_id (int): The ID of the user to operate on.
    """
    if request.method == 'GET':
        try:
            user = user_repository.get_user_by_id(user_id)
            if user: return jsonify(user.to_dict()), 200
            return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            current_app.logger.error(f"Error getting user {user_id}: {e}", exc_info=True)
            return jsonify({'message': 'An unexpected error occurred.'}), 500

    elif request.method == 'PUT':
        data = request.get_json()
        if not data: return jsonify({'message': 'Request body is empty.'}), 400
        try:
            existing = user_repository.get_user_by_id(user_id)
            if not existing: return jsonify({'message': 'User not found'}), 404
            
            # Merge existing data with new data.
            update_data = existing.to_dict()
            update_data.update(data)
            
            # Remove fields that are not expected by the repository's update method.
            update_data.pop('id', None)
            update_data.pop('is_active', None)
            update_data.pop('created_at', None) 

            updated = user_repository.update_user(
                user_id, 
                username=update_data['username'], 
                role=update_data['role'], 
                is_active=update_data['is_active']
            )
            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            current_app.logger.error(f"Error updating user {user_id}: {e}", exc_info=True)
            return jsonify({'message': 'An unexpected error occurred.'}), 500

    elif request.method == 'DELETE':
        try:
            if user_repository.delete_user(user_id):
                return jsonify({'message': 'User deleted successfully'}), 200
            return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            current_app.logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)
            return jsonify({'message': 'An unexpected error occurred.'}), 500

@admin.route('/users/<int:user_id>/reset-password', methods=['PUT'])
@jwt_required()
@role_required('admin')
def reset_user_password(user_id):
    """
    Resets the password for a specific user.
    Requires 'admin' role.

    Args:
        user_id (int): The ID of the user whose password to reset.
    """
    data = request.get_json()
    new_password = data.get('new_password')
    if not new_password:
        return jsonify({'message': 'New password is required'}), 400
    try:
        if user_repository.reset_password(user_id, new_password):
            return jsonify({'message': 'User password reset successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error resetting password for user {user_id}: {e}", exc_info=True)
        return jsonify({'message': 'An unexpected error occurred.'}), 500
# endregion

# region Generic CRUD
def add_crud_routes(endpoint, repo, required_fields, roles):
    """
    Dynamically adds CRUD (Create, Read, Update, Delete) routes for a given entity.

    This function generates standard API endpoints for listing, creating,
    retrieving, updating, and deleting records of a specific type.
    It integrates role-based access control and comprehensive error handling.

    Args:
        endpoint (str): The base URL endpoint for the entity (e.g., 'modules', 'students').
        repo (BaseRepository): The repository instance responsible for database operations of this entity.
        required_fields (list): A list of field names required for creating a new record.
        roles (dict): A dictionary specifying required roles for 'get', 'post', 'put', 'delete' operations.
                      Example: {'get': ['admin', 'course_director'], 'post': 'admin'}
    """
    @admin.route(f'/{endpoint}', methods=['GET', 'POST'], endpoint=f'handle_{endpoint}')
    @jwt_required()
    def handle_list():
        """
        Handles GET (list all) and POST (create new) requests for the generic endpoint.
        """
        if request.method == 'GET':
            @role_required(roles.get('get', ['admin']))
            def get_all():
                """Retrieves all records for the entity."""
                try:
                    records = getattr(repo, f'get_all_{endpoint.replace("-", "_")}')()
                    # Check if records are model instances or dictionaries and convert accordingly.
                    if records and hasattr(records[0], 'to_dict'):
                        return jsonify([r.to_dict() for r in records]), 200
                    else:
                        return jsonify(records), 200 # Directly jsonify if already dictionaries.
                except Exception as e:
                    current_app.logger.error(f"Error getting all {endpoint}: {e}", exc_info=True)
                    return jsonify({'message': 'An unexpected error occurred.'}), 500
            return get_all()
        elif request.method == 'POST':
            @role_required(roles.get('post', 'admin'))
            def create():
                """Creates a new record for the entity."""
                data = request.get_json()
                # Validate required fields for creation.
                if not data or not all(k in data for k in required_fields):
                    return jsonify({'message': f'Missing required fields for {endpoint}.'}), 400
                try:
                    create_method_name = f'create_{endpoint.replace("-", "_").rstrip("s")}'
                    record = getattr(repo, create_method_name)(**data)
                    return jsonify({'message': f'{endpoint} created successfully', 'id': record.id}), 201
                except Exception as e:
                    current_app.logger.error(f"Error creating {endpoint}: {e}", exc_info=True)
                    return jsonify({'message': 'An unexpected error occurred.'}), 500
            return create()

    @admin.route(f'/{endpoint}/<int:record_id>', methods=['GET', 'PUT', 'DELETE'], endpoint=f'handle_single_{endpoint}')
    @jwt_required()
    def handle_single(record_id):
        """
        Handles GET (retrieve single), PUT (update), and DELETE (logical delete)
        requests for a specific record by ID for the generic endpoint.

        Args:
            record_id (int): The ID of the record to operate on.
        """
        if request.method == 'GET':
            @role_required(roles.get('get', ['admin']))
            def get_single(record_id):
                """Retrieves a single record by ID."""
                try:
                    record = getattr(repo, f'get_{endpoint.replace("-", "_").rstrip("s")}_by_id')(record_id)
                    if not record: return jsonify({'message': f'{endpoint} not found'}), 404
                    return jsonify(record.to_dict()), 200
                except Exception as e:
                    current_app.logger.error(f"Error getting {endpoint} {record_id}: {e}", exc_info=True)
                    return jsonify({'message': 'An unexpected error occurred.'}), 500
            return get_single(record_id)
        elif request.method == 'PUT':
            @role_required(roles.get('put', 'admin'))
            def update_single(record_id):
                """Updates an existing record by ID."""
                data = request.get_json()
                if not data: return jsonify({'message': 'Request body is empty.'}), 400
                try:
                    existing = getattr(repo, f'get_{endpoint.replace("-", "_").rstrip("s")}_by_id')(record_id)
                    if not existing: return jsonify({'message': f'{endpoint} not found'}), 404
                    
                    # Dynamically get the update method from the repository.
                    update_method_name = f'update_{endpoint.replace("-", "_").rstrip("s")}'
                    update_method = getattr(repo, update_method_name)
                    
                    # Prepare data for update, merging existing data with new data.
                    update_data = existing.to_dict()
                    update_data.update(data)
                    
                    # Remove fields that are not expected by the repository's update method
                    # or are managed separately (e.g., ID, active status, creation timestamp).
                    update_data.pop('id', None)
                    update_data.pop('is_active', None) 
                    update_data.pop('created_at', None) 
                    
                    # Specific removals based on individual repository update method signatures.
                    if endpoint == 'enrolments':
                        update_data.pop('module_code', None)
                        update_data.pop('module_title', None)
                        update_data.pop('student_name', None) 
                    elif endpoint == 'grades':
                        update_data.pop('module_code', None)
                        update_data.pop('module_title', None)
                        update_data.pop('student_name', None) 
                    elif endpoint == 'attendance-records':
                        update_data.pop('attendance_rate', None)
                        update_data.pop('student_name', None) 
                        update_data.pop('module_code', None) 
                        update_data.pop('module_title', None) 
                    elif endpoint == 'submission-records':
                        update_data.pop('module_code', None)
                        update_data.pop('module_title', None)
                        update_data.pop('student_name', None) 
                    elif endpoint == 'survey-responses':
                        update_data.pop('student_name', None) 
                        update_data.pop('module_code', None)
                        update_data.pop('module_title', None)

                    # Call the update method with the prepared data.
                    updated_record = update_method(record_id, **update_data)
                    
                    return jsonify({'message': f'{endpoint} updated successfully'}), 200
                except Exception as e:
                    current_app.logger.error(f"Error updating {endpoint} {record_id}: {e}", exc_info=True)
                    return jsonify({'message': 'An unexpected error occurred.'}), 500
            return update_single(record_id)
        elif request.method == 'DELETE':
            @role_required(roles.get('delete', 'admin'))
            def delete_single(record_id):
                """Logically deletes a record by ID."""
                try:
                    # Determine whether to perform a hard delete (for alerts) or logical delete.
                    delete_method = getattr(repo, 'delete_hard' if endpoint == 'alerts' else 'delete_logical')
                    if delete_method(record_id):
                        return jsonify({'message': f'{endpoint} deleted successfully'}), 200
                    return jsonify({'message': f'{endpoint} not found'}), 404
                except Exception as e:
                    current_app.logger.error(f"Error deleting {endpoint} {record_id}: {e}", exc_info=True)
                    return jsonify({'message': 'An unexpected error occurred.'}), 500
            return delete_single(record_id)

# Register specific CRUD routes using the generic function.
add_crud_routes('alerts', alert_repository, ['student_id', 'reason'], {'get': ['admin', 'wellbeing_officer'], 'post': 'admin', 'delete': 'admin', 'put': 'admin'})
add_crud_routes('enrolments', enrolment_repository, ['student_id', 'module_id'], {'get': ['admin', 'course_director'], 'post': 'admin', 'delete': 'admin', 'put': 'admin'})
add_crud_routes('grades', grade_repository, ['student_id', 'module_id', 'assessment_name', 'grade'], {'get': ['admin', 'course_director'], 'post': 'admin', 'delete': 'admin', 'put': 'admin'})
add_crud_routes('survey-responses', survey_response_repository, ['student_id', 'week_number', 'stress_level'], {'get': ['admin', 'wellbeing_officer'], 'post': ['admin', 'wellbeing_officer', 'user', 'student'], 'delete': 'admin', 'put': 'admin'})
add_crud_routes('attendance-records', attendance_record_repository, ['student_id', 'module_id', 'week_number'], {'get': ['admin', 'course_director'], 'post': 'admin', 'delete': 'admin', 'put': 'admin'})
add_crud_routes('submission-records', submission_record_repository, ['student_id', 'module_id', 'assessment_name'], {'get': ['admin', 'course_director'], 'post': 'admin', 'delete': 'admin', 'put': 'admin'})
