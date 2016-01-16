import datetime
from builtins import dict

from future.utils import with_metaclass
from core.database import Db, Field


class ModelMeta(type):
    db = Db()

    def __init__(cls, name, what, *fields):
        super().__init__(what)

    def __new__(mcs, name, *fields):
        try:
            Model
        except NameError:
            return type.__new__(mcs, name, *fields)

        sql_fields = dict([(f.field_name, f) for f in fields if isinstance(f, Field)])
        if 'id' not in sql_fields:
            sql_fields['id'] = Field('id', Field.INT, extra_options='PRIMARY KEY AUTOINCREMENT')
        if 'created_at' not in sql_fields:
            sql_fields['created_at'] = Field('created_at', Field.DATETIME, default_value=datetime.datetime.now)
        attributes = {
            'table_name': name,
            'sql_fields': sql_fields,
            '__db': mcs.db
        }
        klass = type.__new__(mcs, name.title(), (Model,), attributes)
        mcs.__create_table__(klass)
        return klass

    @classmethod
    def __create_table__(mcs, klass):
        fields = []
        for field in klass.sql_fields.values():
            fields.append(field.to_sql())
        query = "CREATE TABLE IF NOT EXISTS {table_name} ({fields});" \
            .format(
                table_name=klass.table_name, fields=', '.join(fields))
        mcs.db.execute_sql(query)


class Model(with_metaclass(ModelMeta, object)):
    def __init__(self, *args, **kwargs):
        a = 11

    @classmethod
    def __create_table(cls):
        return {}

    def _crsp(self):
        return self.sql_fields


Version = ModelMeta('version', Field('name', Field.STR, Field.NULL), Field('type', Field.INT))
v1 = Version()
v1

Name = ModelMeta('name', Field('name', Field.STR, Field.NULL))
n1 = Name()
n1
