from core.database import Db


class ModelMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(ModelMeta, cls).__init__(name, bases, nmspc)
        cls.db = classmethod(lambda: Db())


class Field(object):
    STR = 'TEXT'
    DATETIME = 'DATETIME'
    INT = 'INTEGER'
    NULL = 'NULL'
    FLOAT = 'REAL'
    BLOB = 'BLOB'

    def __init__(self, field_name, field_type, default=False):
        self.field_name = field_name
        self.field_type = field_type
        self.default = default

    def field_default(self):
        if self.default is not False:
            return '{0}'.format(self.default)
        return ''

    def to_sql(self):
        return '{field_name} {field_type} {field_default}'.format(field_type=self.field_type,
                                                                  field_name=self.field_name,
                                                                  field_default=self.field_default())


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self, table_name, *fields):
        self.__table = table_name
        self.__fields = fields
        self.__field_list = {f.field_name: f for f in fields}

    def __call__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key in self.__field_list:
                setattr(self, key, value)
        return self

    # todo: move to meta
    def save(self):
        self.db

    def insert(self):
        return '''INSERT INTO {table_name}(fields) VALUES ({placeholders});''' \
            .format(table_name=self.__table, fields=', '.join(f for f in self.__field_list),
                    placeholders=','.join('?' for _ in self.__field_list)), (getattr(self, f) for f in self.__field_list)

    def to_sql(self):
        return '''CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {fields}
        );'''.format(table_name=self.__table, fields=', '.join(map(lambda field: field.to_sql(), self.__fields)))


Version = Model('version', Field('name', Field.STR, Field.NULL), Field('type', Field.INT))

v1 = Version(name=2, b=3)
v1.save()
v1.name

1 == 1
