import os


class Extractor(object):
    def __init__(self):
        self.archive_path =  os.path.abspath('../../dist/')
        self.cmd = '7za.exe l {0} | FINDSTR "[0-9].D....\>" | FIND /V "\\"'

    def extract(self, filename):
        path = self.archive_path + filename

