import sqlite3
from app.db_connection import get_db
from app.models.module import Module
from .base_repository import BaseRepository

class ModuleRepository(BaseRepository):
    def __init__(self):
        super().__init__('modules', Module)

    def get_all_modules(self):
        return super().get_all()

    def get_module_by_id(self, module_id):
        return super().get_by_id(module_id)

    def create_module(self, module_code, module_title, credit, academic_year):
        query = "INSERT INTO modules (module_code, module_title, credit, academic_year, is_active) VALUES (?, ?, ?, ?, 1)"
        module_id = self._execute_insert(query, (module_code, module_title, credit, academic_year))
        return self.get_module_by_id(module_id)

    def update_module(self, module_id, module_code, module_title, credit, academic_year):
        query = "UPDATE modules SET module_code = ?, module_title = ?, credit = ?, academic_year = ? WHERE id = ?"
        self._execute_update_delete(query, (module_code, module_title, credit, academic_year, module_id))
        return self.get_module_by_id(module_id)

    def delete_module(self, module_id):
        return super().delete_logical(module_id)

# Instantiate the repository for use
module_repository = ModuleRepository()
