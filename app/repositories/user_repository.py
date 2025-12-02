"""
User Repository module for managing user data.

This module defines the `UserRepository` class, which provides methods
for interacting with the 'users' table in the database. It extends
`BaseRepository` to handle CRUD operations for users, including
retrieving users by username, creating new users, updating their details,
and resetting passwords.
"""

import sqlite3
from app.db_connection import get_db
from app.models.user import User
from datetime import datetime
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    """
    Repository for user-related database operations.

    Inherits from `BaseRepository` to leverage common CRUD functionality
    and error handling. Provides specific methods for querying and managing
    user accounts.
    """
    def __init__(self):
        """
        Initializes the UserRepository.

        Sets the table name to 'users' and the model class to `User`.
        """
        super().__init__('users', User)

    def get_all_users(self, include_inactive: bool = False) -> list[User]:
        """
        Retrieves all active users from the database.

        Args:
            include_inactive (bool, optional): If True, includes users marked as inactive. Defaults to False.

        Returns:
            list[User]: A list of `User` objects representing all active (or all) users.
        """
        return super().get_all(include_inactive)

    def get_user_by_id(self, user_id: int, include_inactive: bool = False) -> User | None:
        """
        Retrieves a single user by their unique ID.

        Args:
            user_id (int): The unique identifier of the user to retrieve.
            include_inactive (bool, optional): If True, includes inactive users. Defaults to False.

        Returns:
            User | None: A `User` object if found, otherwise None.
        """
        return super().get_by_id(user_id, include_inactive)

    def get_user_by_username(self, username: str, include_inactive: bool = False) -> User | None:
        """
        Retrieves a single user by their username.

        Args:
            username (str): The username to search for.
            include_inactive (bool, optional): If True, includes inactive users. Defaults to False.

        Returns:
            User | None: A `User` object if found, otherwise None.
        """
        query = "SELECT * FROM users WHERE username = ?"
        if not include_inactive:
            query += " AND is_active = 1"
        return self._execute_query(query, (username,), fetch_one=True)

    def create_user(self, username: str, password: str, role: str = 'user', student_id: int | None = None) -> User:
        """
        Creates a new user record in the database.

        The provided plain-text password is hashed before storage.

        Args:
            username (str): The unique username for the new user.
            password (str): The plain-text password for the new user.
            role (str, optional): The role of the new user (e.g., 'user', 'admin', 'student'). Defaults to 'user'.
            student_id (int | None, optional): The ID of an associated student record, if applicable. Defaults to None.

        Returns:
            User: The newly created `User` object.
        """
        new_user = User(username=username, role=role, student_id=student_id)
        new_user.set_password(password) # Hash the password before storing.
        
        query = "INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)"
        user_id = self._execute_insert(query, (new_user.username, new_user.password_hash, new_user.role, new_user.student_id, new_user.created_at.isoformat(), new_user.is_active))
        return self.get_user_by_id(user_id, include_inactive=True)

    def update_user(self, user_id: int, username: str, role: str, is_active: bool) -> User:
        """
        Updates an existing user's information in the database.

        Args:
            user_id (int): The unique identifier of the user to update.
            username (str): The new username for the user.
            role (str): The new role for the user.
            is_active (bool): The new active status for the user.

        Returns:
            User: The updated `User` object.
        """
        query = "UPDATE users SET username = ?, role = ?, is_active = ? WHERE id = ?"
        self._execute_update_delete(query, (username, role, is_active, user_id))
        return self.get_user_by_id(user_id, include_inactive=True)

    def reset_password(self, user_id: int, new_password: str) -> bool:
        """
        Resets a user's password in the database.

        The new plain-text password is hashed before storage.

        Args:
            user_id (int): The unique identifier of the user whose password to reset.
            new_password (str): The new plain-text password.

        Returns:
            bool: True if the password was successfully reset (i.e., a record was updated), False otherwise.
        """
        user = User(id=user_id) # Create a dummy user object to use set_password method.
        user.set_password(new_password) # Hash the new password.
        
        query = "UPDATE users SET password_hash = ? WHERE id = ?"
        return self._execute_update_delete(query, (user.password_hash, user_id))

    def delete_user(self, user_id: int) -> bool:
        """
        Logically deletes a user by setting their 'is_active' flag to 0.

        Args:
            user_id (int): The unique identifier of the user to logically delete.

        Returns:
            bool: True if the user was successfully logically deleted, False otherwise.
        """
        return super().delete_logical(user_id)

# Instantiate the repository for use throughout the application.
user_repository = UserRepository()
