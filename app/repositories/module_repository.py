from app.db_connection import get_db
from app.models.module import Module

class ModuleRepository:
    @staticmethod
    def get_all_modules():
        db = get_db()
        cursor = db.execute("SELECT id, module_code, module_title, credit, academic_year, is_active FROM modules WHERE is_active = 1")
        modules = [Module.from_row(row) for row in cursor.fetchall()]
        return modules

    @staticmethod
    def get_module_by_id(module_id):
        db = get_db()
        cursor = db.execute("SELECT * FROM modules WHERE id = ? AND is_active = 1", (module_id,))
        row = cursor.fetchone()
        return Module.from_row(row) if row else None

    @staticmethod
    def create_module(module_code, module_title, credit, academic_year):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO modules (module_code, module_title, credit, academic_year, is_active) VALUES (?, ?, ?, ?, 1)",
            (module_code, module_title, credit, academic_year)
        )
        db.commit()
        module_id = cursor.lastrowid
        return ModuleRepository.get_module_by_id(module_id)

    @staticmethod
    def update_module(module_id, module_code, module_title, credit, academic_year):
        db = get_db()
        db.execute(
            "UPDATE modules SET module_code = ?, module_title = ?, credit = ?, academic_year = ? WHERE id = ?",
            (module_code, module_title, credit, academic_year, module_id)
        )
        db.commit()
        return ModuleRepository.get_module_by_id(module_id)

    @staticmethod
    def delete_module(module_id):
        db = get_db()
        db.execute("UPDATE modules SET is_active = 0 WHERE id = ?", (module_id,))
        db.commit()
        return True
