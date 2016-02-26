import os
import re
import subprocess

from core.lib import utils


class VarSetter(object):
    def __init__(self):
        self.ruby_path_key = 'RUBY'
        self.path_variable_name = 'PATH'
        self.bat_path = utils.app_path('core/environment')
        self.bat_name = 'setenv.bat'
        self.bat_file = os.path.join(self.bat_path, self.bat_name)
        self.check_local_path_cmd = 'reg query HKCU\Environment /v {variable}'

    def set_version(self, path):
        self._make_path()
        self._set_var(self.ruby_path_key, self.quote(path))

    def _set_var(self, key, value):
        self._create_bat(key, value)
        subprocess.getstatusoutput(self.bat_file)

    def _create_bat(self, key, value):
        command = 'setx %s "%s\n' % (key, value)
        open(self.bat_file, 'w').write(command)

    def _make_path(self):
        # first check the user's path
        status, output = subprocess.getstatusoutput(self.check_local_path_cmd.format(variable=self.path_variable_name))
        if status == 1:
            # error
            self._set_var(self.path_variable_name, '~{0}~'.format(self.ruby_path_key))
        elif status == 0:
            path = ' '.join(re.compile("\s+").split(output.strip("\n").split("\n")[-1].strip(" "))[2:])
            if '%{0}%'.format(self.ruby_path_key) not in path:
                path = self.sanitize_path(path)
                new_path = '%%{0}%%;{1};'.format(self.ruby_path_key, path)
                self._set_var(self.path_variable_name, new_path)

    @staticmethod
    def quote(path):
        return ' ' in path and '\\"{0}\\"'.format(path.replace('"', '')) or path.replace('"', '')

    def sanitize_path(self, path):
        path = ';'.join([self.quote(p) for p in path.split(';')])
        return path.replace('%', '%%')


if __name__ == '__main__':
    v = VarSetter()
    v.set_version('C:\\Program Files\\Python\\bin\\')
