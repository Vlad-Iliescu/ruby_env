import datetime


class Version():
    def __init__(self, version, folder, id=None, date_added=None):
        self.version = version
        self.folder = folder
        self.id = id
        self.date_added = date_added

    @classmethod
    def to_table(cls):
        return '''CREATE TABLE IF NOT EXISTS versions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT,
            folder TEXT,
            date_added DATETIME
        );'''

    @classmethod
    def _prepare_get_id(cls):
        return '''SELECT * FROM versions WHERE (id = ?)'''

    @classmethod
    def _prepare_get_nr(cls):
        return '''SELECT * FROM versions WHERE (version = ?)'''

    def _prepare_insert(self):
        return '''INSERT INTO versions(version, folder, date_added) VALUES ( ?, ?, ? );''', \
               (self.version, self.folder, datetime.datetime.now())