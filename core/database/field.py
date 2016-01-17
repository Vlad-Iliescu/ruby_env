class Field(object):
    STR = 'TEXT'
    DATETIME = 'DATETIME'
    INT = 'INTEGER'
    NULL = 'NULL'
    FLOAT = 'REAL'
    BLOB = 'BLOB'

    def __init__(self, field_name, field_type, default=False, default_value=None, extra_options=None):
        self.field_name = field_name
        self.field_type = field_type
        self.default = default
        self.default_value = default_value
        self.extra_options = extra_options or ''

    def field_default_sql(self):
        if self.default is not False:
            return 'DEFAULT {0}'.format(self.default)
        return ''

    def field_default_value(self):
        if hasattr(self.default_value, '__call__'):
            return self.default_value()
        return self.default_value

    def to_sql(self):
        return \
            '{field_name} {field_type} {field_default} {extra_options}' \
                .format(field_type=self.field_type,
                        field_name=self.field_name,
                        field_default=self.field_default_sql(),
                        extra_options=self.extra_options)
