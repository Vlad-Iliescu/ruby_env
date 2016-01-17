import datetime
from builtins import dict

from future.utils import with_metaclass
from core.database import Db, Field
from core.database.db import RecordNotFound


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
            'db': mcs.db
        }
        for k in sql_fields:
            attributes[k] = None
        klass = type.__new__(mcs, name.title(), (Model,), attributes)
        mcs.__create_table__(klass)
        return klass

    @classmethod
    def __create_table__(mcs, klass):
        fields = []
        for field in klass.sql_fields.values():
            fields.append(field.to_sql())
        mcs.db.create_table(klass.table_name, fields)


class Model(with_metaclass(ModelMeta, object)):
    """
    :type self.sql_fields: dict
    :type self.table_name: str
    :type self.db: Db
    """

    def __init__(self, **kwargs):
        for k in kwargs:
            if k in self.sql_fields:
                setattr(self, k, kwargs[k])

    def save(self):
        keys = []
        values = []
        for k in self.sql_fields:
            keys.append(k)
            values.append(getattr(self, k) or self.sql_fields[k].field_default_value())
        self.id = self.db.insert_or_update_record(self.table_name, keys, values)

    @classmethod
    def find(cls, record_id):
        return cls.find_by('id', record_id)

    @classmethod
    def find_by(cls, key, value):
        record = cls.db.find_record_by(cls.table_name, key, value)
        if record is None:
            raise RecordNotFound()
        return cls(**dict(record))


def create_model(name, *fields):
    return ModelMeta(name, *fields)
