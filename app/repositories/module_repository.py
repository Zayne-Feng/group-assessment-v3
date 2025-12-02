"""
Module Repository module for managing academic module data.

This module defines the `ModuleRepository` class, which provides methods
for interacting with the 'modules' table in the database. It extends
`BaseRepository` to handle CRUD operations for modules, including
retrieving, creating, updating, and logically deleting module records.
"""

import sqlite3
from app.db_connection import get_db
from app.models.module import Module
from .base_repository import BaseRepository

class ModuleRepository(BaseRepository):
    """
    Repository for module-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    academic modules.
    """
    def __init__(self):
        """
        Initializes the ModuleRepository.

        Sets the table name to 'modules' and the model class to `Module`.
        """
        super().__init__('modules', Module)

    def get_all_modules(self) -> list[Module]:
        """
        Retrieves all active modules from the database.

        Returns:
            list[Module]: A list of `Module` objects representing all active modules.
        """
        return super().get_all()

    def get_module_by_id(self, module_id: int) -> Module | None:
        """
        Retrieves a single module by its unique ID.

        Args:
            module_id (int): The unique identifier of the module to retrieve.

        Returns:
            Module | None: A `Module` object if found, otherwise None.
        """
        return super().get_by_id(module_id)

    def create_module(self, module_code: str, module_title: str, credit: int, academic_year: str) -> Module:
        """
        Creates a new module record in the database.

        Args:
            module_code (str): The unique code for the new module.
            module_title (str): The full title or name of the new module.
            credit (int): The credit value of the new module.
            academic_year (str): The academic year in which the module is offered.

        Returns:
            Module: The newly created `Module` object.
        """
        query = "INSERT INTO modules (module_code, module_title, credit, academic_year, is_active) VALUES (?, ?, ?, ?, 1)"
        module_id = self._execute_insert(query, (module_code, module_title, credit, academic_year))
        return self.get_module_by_id(module_id)

    def update_module(self, module_id: int, module_code: str, module_title: str, credit: int, academic_year: str) -> Module:
        """
        Updates an existing module record in the database.

        Args:
            module_id (int): The unique identifier of the module to update.
            module_code (str): The new unique code for the module.
            module_title (str): The new full title or name of the module.
            credit (int): The new credit value of the module.
            academic_year (str): The new academic year in which the module is offered.

        Returns:
            Module: The updated `Module` object.
        """
        query = "UPDATE modules SET module_code = ?, module_title = ?, credit = ?, academic_year = ? WHERE id = ?"
        self._execute_update_delete(query, (module_code, module_title, credit, academic_year, module_id))
        return self.get_module_by_id(module_id)

    def delete_module(self, module_id: int) -> bool:
        """
        Logically deletes a module by setting its 'is_active' flag to 0.

        Args:
            module_id (int): The unique identifier of the module to logically delete.

        Returns:
            bool: True if the module was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(module_id)

# Instantiate the repository for use throughout the application.
module_repository = ModuleRepository()
