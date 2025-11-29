from datetime import datetime
from .base_model import BaseModel

class Module(BaseModel):
    def __init__(self, id=None, module_code=None, module_title=None, credit=None, academic_year=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.module_code = module_code
        self.module_title = module_title
        self.credit = credit
        self.academic_year = academic_year

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'module_code': self.module_code,
            'module_title': self.module_title,
            'credit': self.credit,
            'academic_year': self.academic_year,
        })
        return data

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        row_dict = dict(row)

        # Parse created_at if it's a string
        created_at_str = row_dict.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str

        return cls(
            id=row_dict.get('id'),
            module_code=row_dict.get('module_code'),
            module_title=row_dict.get('module_title'),
            credit=row_dict.get('credit'),
            academic_year=row_dict.get('academic_year'),
            is_active=bool(row_dict.get('is_active')),
            created_at=created_at
        )

    def __repr__(self):
        return f'<Module {self.module_title}>'
