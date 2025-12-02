import pytest
from app.models.base_model import BaseModel
from datetime import datetime

def test_base_model_initialization():
    """Tests the basic initialization of the BaseModel."""
    model = BaseModel(id=1, is_active=False)
    assert model.id == 1
    assert model.is_active is False
    assert isinstance(model.created_at, datetime)

def test_base_model_to_dict():
    """Tests the to_dict method of the BaseModel."""
    now = datetime.now()
    model = BaseModel(id=1, created_at=now)
    model_dict = model.to_dict()
    assert model_dict['id'] == 1
    assert model_dict['is_active'] is True
    assert model_dict['created_at'] == now.isoformat()

def test_base_model_from_row():
    """Tests the from_row class method of the BaseModel."""
    now_iso = datetime.now().isoformat()
    row = {'id': 1, 'is_active': 0, 'created_at': now_iso}
    model = BaseModel.from_row(row)
    assert model.id == 1
    assert model.is_active is False
    assert model.created_at.isoformat() == now_iso

def test_base_model_from_row_with_none():
    """Tests that from_row returns None if the row is None."""
    assert BaseModel.from_row(None) is None
