import os
import re
import subprocess

from core.lib import utils


class Extractor(object):
    def __init__(self):
        self.archive_path = utils.app_path('dist')
        self._7zip = utils.app_path('core/archive/7za.exe')
        self._info_cmd = '%s l {0} | FINDSTR "[0-9].D....\>" | FIND /V "\\"' % self._7zip
        self._extract_cmd = '%s x {0} -y -o{1}' % self._7zip

    def get_abs_path(self, path):
        return os.path.join(self.archive_path, *path.split('/'))

    def get_archived_folder_name(self, filename):
        path = self.get_abs_path(filename)
        raw_output = subprocess.getoutput(self._info_cmd.format(path))
        top_folder = re.sub('\s+', ' ', raw_output).split(' ')[-1]
        return top_folder

    def extract(self, filename, destination):
        archive = self.get_abs_path(filename)
        dest = self.get_abs_path(destination)
        status, output = subprocess.getstatusoutput(self._extract_cmd.format(archive, dest))

        if status != 0:
            raise RuntimeError(output)


if __name__ == '__main__':
    ex = Extractor()
    file = '2.0.0/ruby_2_0_0_p247_x64.7z'
    print(ex.get_archived_folder_name(file))
    print(ex.extract(file, '2.0.0'))
