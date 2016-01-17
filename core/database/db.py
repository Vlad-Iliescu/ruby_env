import os
import sqlite3
import datetime

from future.utils import with_metaclass
from core.lib import Singleton


class DbException(Exception):
    pass


class RecordNotFound(DbException):
    pass


class Db(with_metaclass(Singleton, object)):
    def __init__(self):
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('DATETIME', self.convert_datetime)

        self.db_name = os.path.abspath('../../db/versions.db')
        self.connection = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    @staticmethod
    def adapt_datetime(date_with_time):
        return date_with_time.strftime('%Y%m%d%H%M%S')

    @staticmethod
    def convert_datetime(date_text):
        return datetime.datetime.strptime(date_text.decode('utf-8'), '%Y%m%d%H%M%S')

    @staticmethod
    def process_value(value):
        return value

    def execute_sql(self, sql, parameters=()):
        if not sql:
            return None
        return self.cursor.execute(sql, parameters)

    def create_table(self, table_name, fields):
        query = "CREATE TABLE IF NOT EXISTS {table_name} ({fields});" \
            .format(
                table_name=table_name, fields=', '.join(fields))
        self.execute_sql(query)

    def insert_or_update_record(self, table, keys, values):
        query = "INSERT OR REPLACE INTO {table_name} ({keys}) VALUES ({values_placeholders})" \
            .format(
                table_name=table,
                keys=', '.join(keys),
                values_placeholders=', '.join(['?' for _ in keys])
        )
        self.execute_sql(query, [self.process_value(v) for v in values])
        return self.cursor.lastrowid

    def find_record_by(self, table, key, value):
        query = "SELECT * FROM {table_name} WHERE ({key} = ?)". \
            format(
                table_name=table,
                key=key
        )
        cursor = self.execute_sql(query, [self.process_value(value)])
        return cursor.fetchone()
