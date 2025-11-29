import sqlite3
from app.db_connection import get_db
from app.models.user import User
from datetime import datetime
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__('users', User)

    def get_all_users(self, include_inactive=False):
        return super().get_all(include_inactive)

    def get_user_by_id(self, user_id, include_inactive=False):
        return super().get_by_id(user_id, include_inactive)

    def get_user_by_username(self, username, include_inactive=False):
        query = "SELECT * FROM users WHERE username = ?"
        if not include_inactive:
            query += " AND is_active = 1"
        return self._execute_query(query, (username,), fetch_one=True)

    def create_user(self, username, password, role='user', student_id=None):
        new_user = User(username=username, role=role, student_id=student_id)
        new_user.set_password(password)
        
        query = "INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)"
        user_id = self._execute_insert(query, (new_user.username, new_user.password_hash, new_user.role, new_user.student_id, new_user.created_at.isoformat(), new_user.is_active))
        return self.get_user_by_id(user_id, include_inactive=True)

    def update_user(self, user_id, username, role, is_active):
        query = "UPDATE users SET username = ?, role = ?, is_active = ? WHERE id = ?"
        self._execute_update_delete(query, (username, role, is_active, user_id))
        return self.get_user_by_id(user_id, include_inactive=True)

    def reset_password(self, user_id, new_password):
        user = User(id=user_id)
        user.set_password(new_password)
        
        query = "UPDATE users SET password_hash = ? WHERE id = ?"
        return self._execute_update_delete(query, (user.password_hash, user_id))

    def delete_user(self, user_id):
        return super().delete_logical(user_id)

# Instantiate the repository for use
user_repository = UserRepository()
