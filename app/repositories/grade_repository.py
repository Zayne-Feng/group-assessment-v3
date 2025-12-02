"""
Grade Repository module for managing student grade data.

This module defines the `GradeRepository` class, which provides methods
for interacting with the 'grades' table in the database. It extends
`BaseRepository` to handle CRUD operations for grades, including
retrieving records with joined student and module information.
"""

import sqlite3
from app.db_connection import get_db
from app.models.grade import Grade
from .base_repository import BaseRepository

class GradeRepository(BaseRepository):
    """
    Repository for grade-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    student grades for various assessments.
    """
    def __init__(self):
        """
        Initializes the GradeRepository.

        Sets the table name to 'grades' and the model class to `Grade`.
        """
        super().__init__('grades', Grade)

    def get_all_grades(self) -> list[dict]:
        """
        Retrieves all active grades from the database, including associated
        student and module information for richer context.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents
                        a grade with joined student and module details.
        """
        query = """
            SELECT g.id, g.student_id, g.module_id, g.assessment_name, g.grade, g.is_active,
                   s.full_name as student_name, m.module_title as module_title
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN modules m ON g.module_id = m.id
            WHERE g.is_active = 1
        """
        # _execute_query handles exceptions and returns results as dictionaries due to fetch_all_dicts=True.
        return self._execute_query(query, fetch_all_dicts=True)

    def get_grade_by_id(self, grade_id: int) -> Grade | None:
        """
        Retrieves a single grade by its unique ID.

        Args:
            grade_id (int): The unique identifier of the grade to retrieve.

        Returns:
            Grade | None: A `Grade` object if found, otherwise None.
        """
        return super().get_by_id(grade_id)

    def create_grade(self, student_id: int, module_id: int, assessment_name: str, grade: float) -> Grade:
        """
        Creates a new grade record in the database.

        Args:
            student_id (int): The ID of the student receiving the grade.
            module_id (int): The ID of the module for which the grade is given.
            assessment_name (str): The name of the assessment (e.g., 'Final Exam', 'Assignment 1').
            grade (float): The numerical grade value.

        Returns:
            Grade: The newly created `Grade` object.
        """
        query = "INSERT INTO grades (student_id, module_id, assessment_name, grade, is_active) VALUES (?, ?, ?, ?, 1)"
        grade_id = self._execute_insert(query, (student_id, module_id, assessment_name, grade))
        return self.get_grade_by_id(grade_id)

    def update_grade(self, grade_id: int, student_id: int, module_id: int, assessment_name: str, grade: float) -> Grade:
        """
        Updates an existing grade record in the database.

        Args:
            grade_id (int): The unique identifier of the grade to update.
            student_id (int): The new student ID for the grade.
            module_id (int): The new module ID for the grade.
            assessment_name (str): The new assessment name for the grade.
            grade (float): The new numerical grade value.

        Returns:
            Grade: The updated `Grade` object.
        """
        query = "UPDATE grades SET student_id = ?, module_id = ?, assessment_name = ?, grade = ? WHERE id = ?"
        self._execute_update_delete(query, (student_id, module_id, assessment_name, grade, grade_id))
        return self.get_grade_by_id(grade_id)

    def delete_grade(self, grade_id: int) -> bool:
        """
        Logically deletes a grade by setting its 'is_active' flag to 0.

        Args:
            grade_id (int): The unique identifier of the grade to logically delete.

        Returns:
            bool: True if the grade was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(grade_id)

# Instantiate the repository for use throughout the application.
grade_repository = GradeRepository()
