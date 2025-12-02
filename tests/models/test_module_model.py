import pytest
from app.models.module import Module
from datetime import datetime

def test_module_initialization():
    """Tests the initialization of the Module model."""
    module = Module(id=1, module_code='CS101', module_title='Intro to CS', credit=15, academic_year='2025')
    assert module.id == 1
    assert module.module_title == 'Intro to CS'

def test_module_to_dict():
    """Tests the to_dict method of the Module model."""
    now = datetime.now()
    module = Module(id=1, module_title='Intro to CS', created_at=now)
    module_dict = module.to_dict()
    assert module_dict['id'] == 1
    assert module_dict['module_title'] == 'Intro to CS'
    assert module_dict['created_at'] == now.isoformat()

def test_module_from_row():
    """Tests the from_row class method of the Module model."""
    now_iso = datetime.now().isoformat()
    row = {
        'id': 1,
        'module_code': 'CS101',
        'module_title': 'Intro to CS',
        'credit': 15,
        'academic_year': '2025',
        'is_active': 1,
        'created_at': now_iso
    }
    module = Module.from_row(row)
    assert module.id == 1
    assert module.module_title == 'Intro to CS'
    assert module.created_at.isoformat() == now_iso
