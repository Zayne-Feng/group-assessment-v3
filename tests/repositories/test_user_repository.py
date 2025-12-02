import pytest
from app.repositories.user_repository import user_repository

def test_create_user_in_db():
    """
    Integration test to verify user creation in the database.
    """
    new_user = user_repository.create_user('repo_test_user', 'password123', 'user')
    assert new_user is not None
    assert new_user.id is not None
    assert new_user.username == 'repo_test_user'

    # Verify by fetching the user back from the DB
    fetched_user = user_repository.get_user_by_id(new_user.id)
    assert fetched_user is not None
    assert fetched_user.username == 'repo_test_user'

def test_get_user_by_username_from_db():
    """
    Integration test to verify fetching a user by username from the database.
    """
    # The 'admin' user is created by the seed data
    user = user_repository.get_user_by_username('admin')
    assert user is not None
    assert user.username == 'admin'
    assert user.role == 'admin'

def test_update_user_in_db():
    """
    Integration test to verify updating a user in the database.
    """
    # Create a user to update
    user_to_update = user_repository.create_user('update_me', 'password', 'user')
    
    # Update the user's role
    updated_user = user_repository.update_user(user_to_update.id, 'update_me_updated', 'admin', True)
    assert updated_user is not None
    assert updated_user.role == 'admin'
    assert updated_user.username == 'update_me_updated'

    # Verify the update by fetching again
    fetched_user = user_repository.get_user_by_id(user_to_update.id)
    assert fetched_user.role == 'admin'

def test_delete_user_in_db():
    """
    Integration test to verify logical deletion of a user in the database.
    """
    # Create a user to delete
    user_to_delete = user_repository.create_user('delete_me', 'password', 'user')
    
    # Perform a logical delete
    delete_success = user_repository.delete_user(user_to_delete.id)
    assert delete_success is True

    # Verify the user is inactive (should not be found by default)
    fetched_user = user_repository.get_user_by_id(user_to_delete.id)
    assert fetched_user is None

    # Verify the user can be found if inactive records are included
    inactive_user = user_repository.get_user_by_id(user_to_delete.id, include_inactive=True)
    assert inactive_user is not None
    assert inactive_user.is_active is False
