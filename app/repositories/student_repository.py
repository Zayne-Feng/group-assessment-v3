"""
Student Repository module for managing student data.

This module defines the `StudentRepository` class, which provides methods
for interacting with the 'students' table in the database. It extends
`BaseRepository` to handle CRUD operations for students, including
retrieving student details and their associated enrolments.
"""

import sqlite3
from app.db_connection import get_db
from app.models.student import Student
from .base_repository import BaseRepository
from flask import current_app # Import current_app for logging

class StudentRepository(BaseRepository):
    """
    Repository for student-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student records.
    """
    def __init__(self):
        """
        Initializes the StudentRepository.

        Sets the table name to 'students' and the model class to `Student`.
        """
        super().__init__('students', Student)

    def get_all_students(self, include_inactive: bool = False) -> list[Student]:
        """
        Retrieves all active students from the database.

        Args:
            include_inactive (bool, optional): If True, includes students marked as inactive. Defaults to False.

        Returns:
            list[Student]: A list of `Student` objects representing all active (or all) students.
        """
        return super().get_all(include_inactive)

    def get_student_by_id(self, student_id: int, include_inactive: bool = False) -> Student | None:
        """
        Retrieves a single student by their unique ID.

        Args:
            student_id (int): The unique identifier of the student to retrieve.
            include_inactive (bool, optional): If True, includes inactive students. Defaults to False.

        Returns:
            Student | None: A `Student` object if found, otherwise None.
        """
        return super().get_by_id(student_id, include_inactive)

    def get_student_by_student_number(self, student_number: str) -> Student | None:
        """
        Retrieves a single student by their unique student number.

        Args:
            student_number (str): The student number to search for.

        Returns:
            Student | None: A `Student` object if found, otherwise None.
        """
        query = "SELECT * FROM students WHERE student_number = ? AND is_active = 1"
        return self._execute_query(query, (student_number,), fetch_one=True)

    def get_student_enrolments(self, student_id: int) -> list[dict]:
        """
        Retrieves all active enrolments for a specific student, including module details.

        Args:
            student_id (int): The unique identifier of the student.

        Returns:
            list[dict]: A list of dictionaries, each representing an enrolment
                        with associated module code and title.
        """
        query = """
            SELECT e.id, e.student_id, e.module_id, e.enrol_date, e.is_active,
                   m.module_code, m.module_title
            FROM enrolments e
            JOIN modules m ON e.module_id = m.id
            WHERE e.student_id = ? AND e.is_active = 1
        """
        # This method directly uses get_db() and db.execute(), so it needs its own try-except.
        # The _execute_query method in BaseRepository would also work here.
        try:
            db = get_db()
            cursor = db.execute(query, (student_id,))
            enrolments = []
            for row in cursor.fetchall():
                enrolments.append({
                    'id': row['id'],
                    'module_id': row['module_id'],
                    'module_code': row['module_code'],
                    'module_title': row['module_title'],
                    'enrol_date': row['enrol_date']
                })
            return enrolments
        except sqlite3.Error as e:
            current_app.logger.error(f"Database error in get_student_enrolments for student {student_id}: {e}", exc_info=True)
            raise Exception(f"Could not retrieve enrolments for student {student_id}.")

    def create_student(self, student_number: str, full_name: str, email: str, course_name: str | None, year_of_study: int | None) -> Student:
        """
        Creates a new student record in the database.

        Args:
            student_number (str): The unique student number.
            full_name (str): The full name of the student.
            email (str): The email address of the student.
            course_name (str | None): The name of the course the student is enrolled in.
            year_of_study (int | None): The student's current year of study.

        Returns:
            Student: The newly created `Student` object.
        """
        query = "INSERT INTO students (student_number, full_name, email, course_name, year_of_study, is_active) VALUES (?, ?, ?, ?, ?, 1)"
        student_id = self._execute_insert(query, (student_number, full_name, email, course_name, year_of_study))
        return self.get_student_by_id(student_id)

    def update_student(self, student_id: int, student_number: str, full_name: str, email: str, course_name: str | None, year_of_study: int | None) -> Student:
        """
        Updates an existing student's information in the database.

        Args:
            student_id (int): The unique identifier of the student to update.
            student_number (str): The new unique student number.
            full_name (str): The new full name of the student.
            email (str): The new email address of the student.
            course_name (str | None): The new course name.
            year_of_study (int | None): The new year of study.

        Returns:
            Student: The updated `Student` object.
        """
        query = "UPDATE students SET student_number = ?, full_name = ?, email = ?, course_name = ?, year_of_study = ? WHERE id = ?"
        self._execute_update_delete(query, (student_number, full_name, email, course_name, year_of_study, student_id))
        return self.get_student_by_id(student_id)

    def delete_student(self, student_id: int) -> bool:
        """
        Logically deletes a student by setting their 'is_active' flag to 0.

        Args:
            student_id (int): The unique identifier of the student to logically delete.

        Returns:
            bool: True if the student was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(student_id)

    def delete_student_hard(self, student_id: int) -> bool:
        """
        Permanently deletes a student record from the database.

        Use this method with caution, as data deleted this way cannot be recovered.

        Args:
            student_id (int): The unique identifier of the student to permanently delete.

        Returns:
            bool: True if the student was successfully permanently deleted, False otherwise.
        """
        return super().delete_hard(student_id)

# Instantiate the repository for use throughout the application.
student_repository = StudentRepository()
