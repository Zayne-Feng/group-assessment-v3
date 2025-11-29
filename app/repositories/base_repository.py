import sqlite3
from app.db_connection import get_db

class BaseRepository:
    def __init__(self, table_name, model_class):
        self.table_name = table_name
        self.model_class = model_class

    def _execute_query(self, query, params=(), fetch_one=False, fetch_all_dicts=False):
        db = get_db()
        try:
            cursor = db.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                if row:
                    # If it's a single value (e.g., COUNT, AVG), return the value directly
                    if len(row) == 1 and not fetch_all_dicts:
                        return row[0]
                    return dict(row) if fetch_all_dicts or self.model_class is None else self.model_class.from_row(row)
                return None
            else:
                rows = cursor.fetchall()
                if fetch_all_dicts or self.model_class is None:
                    return [dict(row) for row in rows]
                return [self.model_class.from_row(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error in {self.table_name} repository: {e}")
            raise Exception(f"Database operation failed for {self.table_name}.")

    def _execute_insert(self, query, params=()):
        db = get_db()
        try:
            cursor = db.execute(query, params)
            db.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error in {self.table_name} repository (insert): {e}")
            raise Exception(f"Failed to insert into {self.table_name}.")

    def _execute_update_delete(self, query, params=()):
        db = get_db()
        try:
            db.execute(query, params)
            db.commit()
            return True
        except sqlite3.Error as e:
            db.rollback()
            print(f"Database error in {self.table_name} repository (update/delete): {e}")
            raise Exception(f"Failed to update/delete from {self.table_name}.")

    def get_all(self, include_inactive=False):
        query = f"SELECT * FROM {self.table_name}"
        if not include_inactive:
            query += " WHERE is_active = 1"
        return self._execute_query(query)

    def get_by_id(self, item_id, include_inactive=False):
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        if not include_inactive:
            query += " AND is_active = 1"
        return self._execute_query(query, (item_id,), fetch_one=True)

    def delete_logical(self, item_id):
        query = f"UPDATE {self.table_name} SET is_active = 0 WHERE id = ?"
        return self._execute_update_delete(query, (item_id,))

    def delete_hard(self, item_id):
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute_update_delete(query, (item_id,))
