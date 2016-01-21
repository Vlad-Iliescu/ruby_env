import os
import re
import subprocess


class Extractor(object):
    def __init__(self):
        self.archive_path = os.path.abspath('../../dist/')
        self._7zip = path = os.path.abspath('7za.exe')
        self.cmd = '%s l {0} | FINDSTR "[0-9].D....\>" | FIND /V "\\"' % self._7zip

    def extract(self, filename):
        path = os.path.join(self.archive_path, filename)

    def get_archived_folder_name(self, filename):
        path = os.path.join(self.archive_path, *filename.split('/'))
        raw_output = subprocess.getoutput(self.cmd.format(path))
        top_folder = re.sub('\s+', ' ', raw_output).split(' ')[-1]
        return top_folder

if __name__ == '__main__':
    ex = Extractor()
    print(ex.get_archived_folder_name('2.0.0/ruby_2_0_0_p247_x64.7z'))