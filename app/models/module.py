class Module:
    def __init__(self, id=None, module_code=None, module_title=None, credit=None, academic_year=None, is_active=True):
        self.id = id
        self.module_code = module_code
        self.module_title = module_title
        self.credit = credit
        self.academic_year = academic_year
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'module_code': self.module_code,
            'module_title': self.module_title,
            'credit': self.credit,
            'academic_year': self.academic_year,
            'is_active': self.is_active
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Module(
            id=row['id'],
            module_code=row['module_code'],
            module_title=row['module_title'],
            credit=row['credit'],
            academic_year=row['academic_year'],
            is_active=bool(row['is_active'])
        )

    def __repr__(self):
        return f'<Module {self.module_title}>'
