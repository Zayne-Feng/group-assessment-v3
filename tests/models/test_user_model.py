"""
Unit tests for the User model.

This module tests the creation of User instances, password hashing and verification,
and data serialization methods of the User model.
"""

import pytest
from app.models.user import User

def test_user_creation():
    """
    Tests the basic creation of a User instance and its default attributes.
    """
    user = User(username='testuser', role='user')
    assert user.username == 'testuser'
    assert user.role == 'user'
    assert user.password_hash is None
    assert user.is_active is True
    assert user.student_id is None

def test_password_hashing():
    """
    Tests that the set_password method correctly hashes the password.
    """
    user = User(username='hashuser')
    user.set_password('mysecretpassword')
    
    # The password hash should not be None after setting it.
    assert user.password_hash is not None
    # The hash should not be the same as the original password.
    assert user.password_hash != 'mysecretpassword'

def test_password_verification():
    """
    Tests that check_password correctly verifies a correct and incorrect password.
    """
    user = User(username='checkpassuser')
    password = 'supersecret'
    user.set_password(password)
    
    # Check that the correct password returns True.
    assert user.check_password(password) is True
    # Check that an incorrect password returns False.
    assert user.check_password('wrongpassword') is False
    # Check that an empty password returns False.
    assert user.check_password('') is False

def test_password_verification_no_hash():
    """
    Tests that check_password returns False if no password hash is set.
    """
    user = User(username='nohashuser')
    # The password_hash is None by default.
    assert user.check_password('anypassword') is False

def test_user_to_dict():
    """
    Tests the to_dict method for correct dictionary representation.
    """
    user = User(id=1, username='dictuser', role='admin', student_id=5)
    user_dict = user.to_dict()
    
    expected_keys = ['id', 'username', 'role', 'student_id', 'is_active', 'created_at']
    for key in expected_keys:
        assert key in user_dict
        
    assert user_dict['username'] == 'dictuser'
    assert user_dict['role'] == 'admin'
    assert user_dict['student_id'] == 5
    assert user_dict['id'] == 1
    # The password hash should not be included in the dictionary representation.
    assert 'password_hash' not in user_dict
