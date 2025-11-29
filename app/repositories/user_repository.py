from app.db_connection import get_db
from app.models.user import User
from datetime import datetime

class UserRepository:
    @staticmethod
    def get_all_users(include_inactive=False):
        db = get_db()
        sql = "SELECT * FROM users"
        if not include_inactive:
            sql += " WHERE is_active = 1"
        cursor = db.execute(sql)
        users = [User.from_row(row) for row in cursor.fetchall()]
        return users

    @staticmethod
    def get_user_by_id(user_id, include_inactive=False):
        db = get_db()
        sql = "SELECT * FROM users WHERE id = ?"
        params = (user_id,)
        
        if not include_inactive:
            sql += " AND is_active = 1"
            
        cursor = db.execute(sql, params)
        row = cursor.fetchone()
        return User.from_row(row) if row else None

    @staticmethod
    def get_user_by_username(username, include_inactive=False):
        db = get_db()
        sql = "SELECT * FROM users WHERE username = ?"
        params = (username,)

        if not include_inactive:
            sql += " AND is_active = 1"

        cursor = db.execute(sql, params)
        row = cursor.fetchone()
        return User.from_row(row) if row else None

    @staticmethod
    def create_user(username, password, role='user', student_id=None):
        db = get_db()
        new_user = User(username=username, role=role, student_id=student_id)
        new_user.set_password(password)
        
        cursor = db.execute(
            "INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            (new_user.username, new_user.password_hash, new_user.role, new_user.student_id, new_user.created_at.isoformat(), new_user.is_active)
        )
        db.commit()
        new_user_id = cursor.lastrowid
        return UserRepository.get_user_by_id(new_user_id, include_inactive=True)

    @staticmethod
    def update_user(user_id, username, role, is_active):
        db = get_db()
        db.execute(
            "UPDATE users SET username = ?, role = ?, is_active = ? WHERE id = ?",
            (username, role, is_active, user_id)
        )
        db.commit()
        return UserRepository.get_user_by_id(user_id, include_inactive=True)

    @staticmethod
    def reset_password(user_id, new_password):
        db = get_db()
        user = User(id=user_id)
        user.set_password(new_password)
        
        db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (user.password_hash, user_id)
        )
        db.commit()
        return True

    @staticmethod
    def delete_user(user_id):
        db = get_db()
        db.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
        db.commit()
        return True
