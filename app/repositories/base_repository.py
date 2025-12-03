"""
Base repository module for common database operations.

This module defines the `BaseRepository` class, which provides a standardized
interface for interacting with a specific database table. It encapsulates
common CRUD (Create, Read, Update, Delete) operations and includes robust
error handling and transaction management using SQLite.
"""

import sqlite3
from app.db_connection import get_db
from flask import current_app # Import current_app for logging

class BaseRepository:
    """
    A base repository class providing common database operations for a specific table.

    This class is designed to be inherited by other specific repositories
    (e.g., `UserRepository`, `ModuleRepository`) to centralize database
    interaction logic, error handling, and transaction management.
    """
    def __init__(self, table_name, model_class):
        """
        Initializes the BaseRepository instance.

        Args:
            table_name (str): The name of the database table this repository manages.
            model_class: The model class (e.g., `User`, `Module`) that this
                         repository maps database rows to. If None, results are returned as dictionaries.
        """
        self.table_name = table_name
        self.model_class = model_class

    def _execute_query(self, query, params=(), fetch_one=False, fetch_all_dicts=False):
        """
        Executes a SELECT query and returns the results, optionally mapping them to model instances.

        Args:
            query (str): The SQL SELECT query string to execute.
            params (tuple, optional): A tuple of parameters to bind to the query. Defaults to an empty tuple.
            fetch_one (bool, optional): If True, fetches only the first matching row. Defaults to False.
            fetch_all_dicts (bool, optional): If True, returns results as a list of dictionaries.
                                             Overrides `model_class` if True. Defaults to False.

        Returns:
            Union[Any, List[Any], None]:
                - If `fetch_one` is True: A single model instance, a dictionary, a single value, or None.
                - If `fetch_one` is False: A list of model instances, a list of dictionaries, or an empty list.

        Raises:
            Exception: If a `sqlite3.Error` occurs during query execution,
                       it's caught, logged, and re-raised as a generic Exception.
        """
        db = get_db()
        try:
            cursor = db.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                if row:
                    # If only one column is selected and not explicitly asking for dict, return the scalar value.
                    if len(row) == 1 and not fetch_all_dicts:
                        return row[0]
                    # Return as dict or model instance based on flags and model_class availability.
                    return dict(row) if fetch_all_dicts or self.model_class is None else self.model_class.from_row(row)
                return None # No row found.
            else:
                rows = cursor.fetchall()
                # Return as list of dicts or list of model instances.
                return [dict(row) for row in rows] if fetch_all_dicts or self.model_class is None else [self.model_class.from_row(row) for row in rows]
        except sqlite3.Error as e:
            # Log the specific database error with full traceback.
            current_app.logger.error(f"Database error in {self.table_name} repository (query): {e}", exc_info=True)
            # Re-raise as a generic exception for higher layers to handle.
            raise Exception(f"Database operation failed for {self.table_name}.")

    def _execute_insert(self, query, params=()):
        """
        Executes an INSERT query and returns the ID of the newly inserted row.

        This method ensures that the transaction is committed on success
        and rolled back on failure.

        Args:
            query (str): The SQL INSERT query string to execute.
            params (tuple, optional): A tuple of parameters to bind to the query. Defaults to an empty tuple.

        Returns:
            int: The `lastrowid` (ID of the newly inserted row) if the insertion is successful.

        Raises:
            Exception: If a `sqlite3.Error` occurs during insertion,
                       the transaction is rolled back, the error is logged, and re-raised.
        """
        db = get_db()
        try:
            cursor = db.execute(query, params)
            return cursor.lastrowid
        except sqlite3.Error as e:
            current_app.logger.error(f"Database error in {self.table_name} repository (insert): {e}", exc_info=True)
            raise Exception(f"Failed to insert into {self.table_name}.")

    def _execute_update_delete(self, query, params=()):
        """
        Executes an UPDATE or DELETE query.

        This method ensures that the transaction is committed on success
        and rolled back on failure.

        Args:
            query (str): The SQL UPDATE or DELETE query string to execute.
            params (tuple, optional): A tuple of parameters to bind to the query. Defaults to an empty tuple.

        Returns:
            bool: True if the operation was successful and affected at least one row, False otherwise.

        Raises:
            Exception: If a `sqlite3.Error` occurs during the operation,
                       the transaction is rolled back, the error is logged, and re-raised.
        """
        db = get_db()
        try:
            cursor = db.execute(query, params)
            return cursor.rowcount > 0 # Indicates if any row was affected by the operation.
        except sqlite3.Error as e:
            current_app.logger.error(f"Database error in {self.table_name} repository (update/delete): {e}", exc_info=True)
            raise Exception(f"Failed to update/delete from {self.table_name}.")

    def get_all(self, include_inactive=False):
        """
        Retrieves all records from the managed table.

        Args:
            include_inactive (bool, optional): If True, includes records marked as inactive. Defaults to False.

        Returns:
            list: A list of model instances (or dictionaries if `model_class` is None)
                  representing all active records, or all records if `include_inactive` is True.
        """
        query = f"SELECT * FROM {self.table_name}"
        if not include_inactive:
            query += " WHERE is_active = 1"
        return self._execute_query(query)

    def get_by_id(self, item_id, include_inactive=False):
        """
        Retrieves a single record by its ID from the managed table.

        Args:
            item_id (int): The ID of the record to retrieve.
            include_inactive (bool, optional): If True, includes records marked as inactive. Defaults to False.

        Returns:
            Any: A single model instance (or dictionary) if found, otherwise None.
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        if not include_inactive:
            query += " AND is_active = 1"
        return self._execute_query(query, (item_id,), fetch_one=True)

    def delete_logical(self, item_id):
        """
        Performs a logical delete on a record by setting its 'is_active' flag to 0.

        This method is preferred over hard deletion to preserve historical data
        and maintain referential integrity.

        Args:
            item_id (int): The ID of the record to logically delete.

        Returns:
            bool: True if the logical delete operation was successful and affected a record, False otherwise.
        """
        query = f"UPDATE {self.table_name} SET is_active = 0 WHERE id = ?"
        return self._execute_update_delete(query, (item_id,))

    def delete_hard(self, item_id):
        """
        Performs a hard delete on a record, permanently removing it from the database.

        Use this method with caution, as data deleted this way cannot be recovered.

        Args:
            item_id (int): The ID of the record to permanently delete.

        Returns:
            bool: True if the hard delete operation was successful and affected a record, False otherwise.
        """
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute_update_delete(query, (item_id,))
