import pytest
from app.repositories.module_repository import module_repository

def test_create_and_get_module():
    """
    Tests that a module can be created and then retrieved from the database.
    """
    # Create a new module
    new_module = module_repository.create_module(
        module_code='REPO_TEST1',
        module_title='Repository Testing 101',
        credit=15,
        academic_year='2025/2026'
    )
    assert new_module is not None
    assert new_module.id is not None
    
    # Retrieve the module by ID
    fetched_module = module_repository.get_module_by_id(new_module.id)
    assert fetched_module is not None
    assert fetched_module.module_title == 'Repository Testing 101'

def test_update_module_in_db():
    """
    Tests that a module's details can be updated in the database.
    """
    # Create a module to update
    module_to_update = module_repository.create_module(
        module_code='REPO_UPDATE1',
        module_title='Initial Title',
        credit=10,
        academic_year='2025/2026'
    )
    
    # Update the module
    updated_module = module_repository.update_module(
        module_id=module_to_update.id,
        module_code='REPO_UPDATE1_NEW',
        module_title='Updated Title',
        credit=20,
        academic_year='2026/2027'
    )
    assert updated_module is not None
    assert updated_module.module_title == 'Updated Title'
    assert updated_module.credit == 20
    
    # Verify by fetching again
    fetched_module = module_repository.get_module_by_id(module_to_update.id)
    assert fetched_module.module_title == 'Updated Title'
