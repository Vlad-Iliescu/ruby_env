import sqlite3
import datetime

from core.database import Version
from core.lib import Singleton


class Db():
    __metaclass__ = Singleton

    def __init__(self):
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('DATETIME', self.convert_datetime)

        self.db_name = 'versions.db'
        self.connection = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # self._make_structure()


    @staticmethod
    def adapt_datetime(date_with_time):
        return date_with_time.strftime('%Y%m%d%H%M%S')

    @staticmethod
    def convert_datetime(date_text):
        return datetime.datetime.strptime(date_text, '%Y%m%d%H%M%S')

    def _make_structure(self):
        self.cursor.execute(Version.to_table())

    def insert_record(self, record):
        query, params = record.insert()
        self.cursor.execute(query, params)
        record.id = self.cursor.lastrowid

    def execute_sql(self, sql):
        if not sql:
            return None
        return self.cursor.execute(sql)


    # #######################
    # #  Version Model
    # #######################

    def save_version(self, version):
        query = version._prepare_insert()
        self.cursor.execute(*query)
        version.id = self.cursor.lastrowid
        version.date_added = query[1][2]

    def get_version_by_id(self, id):
        self.cursor.execute(Version._prepare_get_id(), (id,))
        result = self.cursor.fetchone()
        return Version(result['version'], result['folder'], result['id'], result['date_added'])

    def get_version_by_nr(self, nr):
        self.cursor.execute(Version._prepare_get_nr(), (nr,))
        result = self.cursor.fetchone()
        return Version(result['version'], result['folder'], result['id'], result['date_added'])



if __name__ == '__main__':
    db = Db()
    version = Version('1.2', '/there')
    db.save_version(version)
    r = db.get_version_by_id(2)
    r = db.get_version_by_nr('1.2')


