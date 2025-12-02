import pytest
import sqlite3
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.db_connection import get_db
from app.models.user import User # Import a sample model for testing

class DummyModel:
    """A dummy model for testing purposes."""
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(row['id'], row['name'])

def test_execute_query_fetch_one_no_model(app):
    """
    Tests _execute_query with fetch_one=True and no model_class, returning a dict.
    """
    with app.app_context():
        repo = BaseRepository('users', None) # No model class
        # Assuming 'users' table exists and has at least one record from seed data
        result = repo._execute_query("SELECT id, username FROM users LIMIT 1", fetch_one=True)
        assert isinstance(result, dict)
        assert 'id' in result
        assert 'username' in result

def test_execute_query_fetch_all_no_model(app):
    """
    Tests _execute_query with no model_class, returning a list of dicts.
    """
    with app.app_context():
        repo = BaseRepository('users', None) # No model class
        result = repo._execute_query("SELECT id, username FROM users LIMIT 2")
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], dict)

def test_execute_query_fetch_one_single_value(app):
    """
    Tests _execute_query with fetch_one=True and a single column query.
    """
    with app.app_context():
        repo = BaseRepository('users', None) # No model class
        result = repo._execute_query("SELECT COUNT(id) FROM users", fetch_one=True)
        assert isinstance(result, int)
        assert result > 0

def test_execute_query_with_model(app):
    """
    Tests _execute_query with a model_class.
    """
    with app.app_context():
        repo = BaseRepository('users', User)
        result = repo._execute_query("SELECT id, username, password_hash, role, created_at, is_active FROM users LIMIT 1", fetch_one=True)
        assert isinstance(result, User)
        assert result.username is not None

def test_execute_query_no_results(app):
    """
    Tests _execute_query when no results are found.
    """
    with app.app_context():
        repo = BaseRepository('users', None)
        result = repo._execute_query("SELECT id FROM users WHERE id = 999999", fetch_one=True)
        assert result is None

def test_execute_insert_rollback(app, mocker):
    """
    Tests that _execute_insert rolls back on error.
    """
    with app.app_context():
        # Create explicit mock objects for connection methods
        mock_cursor = mocker.Mock()
        mock_execute = mocker.Mock(return_value=mock_cursor, side_effect=sqlite3.Error("Test error"))
        mock_rollback = mocker.Mock()
        mock_commit = mocker.Mock()
        
        mock_conn = mocker.Mock()
        mock_conn.execute = mock_execute
        mock_conn.rollback = mock_rollback
        mock_conn.commit = mock_commit
        
        # Patch sqlite3.connect directly
        mocker.patch('app.db_connection.sqlite3.connect', return_value=mock_conn)
        
        repo = BaseRepository('test_table', None)
        with pytest.raises(Exception, match="Failed to insert into test_table."):
            repo._execute_insert("INSERT INTO test_table VALUES (?)", (1,))
        
        mock_rollback.assert_called_once()
        mock_commit.assert_not_called()

def test_execute_update_delete_rollback(app, mocker):
    """
    Tests that _execute_update_delete rolls back on error.
    """
    with app.app_context():
        # Create explicit mock objects for connection methods
        mock_cursor = mocker.Mock()
        mock_execute = mocker.Mock(return_value=mock_cursor, side_effect=sqlite3.Error("Test error"))
        mock_rollback = mocker.Mock()
        mock_commit = mocker.Mock()
        
        mock_conn = mocker.Mock()
        mock_conn.execute = mock_execute
        mock_conn.rollback = mock_rollback
        mock_conn.commit = mock_commit
        
        # Patch sqlite3.connect directly
        mocker.patch('app.db_connection.sqlite3.connect', return_value=mock_conn)
        
        repo = BaseRepository('test_table', None)
        with pytest.raises(Exception, match="Failed to update/delete from test_table."):
            repo._execute_update_delete("UPDATE test_table SET col = ? WHERE id = ?", (1, 1))
        
        mock_rollback.assert_called_once()
        mock_commit.assert_not_called()

def test_delete_hard(app):
    """
    Tests the delete_hard method.
    """
    with app.app_context():
        # Create a dummy record
        db = get_db()
        cursor = db.execute("INSERT INTO users (username, password_hash, role, created_at, is_active) VALUES (?, ?, ?, ?, ?)",
                            ('hard_delete_user', 'hash', 'user', datetime.now().isoformat(), 1))
        user_id = cursor.lastrowid
        db.commit()

        repo = BaseRepository('users', User)
        delete_success = repo.delete_hard(user_id)
        assert delete_success is True

        # Verify it's completely gone
        result = repo._execute_query("SELECT id FROM users WHERE id = ?", (user_id,), fetch_one=True)
        assert result is None
