import os
import subprocess

import re

from core.lib import utils


class VarSetter(object):
    def __init__(self):
        self.ruby_path_key = 'RUBY'
        self.path_variable_name = 'PATHX'
        self.bat_path = utils.app_path('core/environment')
        self.bat_name = 'setenv.bat'
        self.bat_file = os.path.join(self.bat_path, self.bat_name)
        self.check_local_path_cmd = 'reg query HKCU\Environment /v {variable}'

    def set_version(self, path):
        self._make_path()
        self._set_var(self.ruby_path_key, path)

    def _set_var(self, key, value):
        self._create_bat(key, value)
        status, output = subprocess.getstatusoutput(self.bat_file)

    def _create_bat(self, key, value):
        command = 'setx %s %s\n' % (key, value)
        open(self.bat_file, 'w').write(command)

    def _make_path(self):
        # return
        # # fixme: path escape problems for paths with spaces
        # if os.environ.get(self.ruby_path_key) is None:
        #     self._set_var('PATH', '"{0};%{1}%;"'.format(
        #         os.environ.get('PATH').replace('"', '\\"').rstrip(';'), self.ruby_path_key
        #     ))

        # first check the user's path
        status, output = subprocess.getstatusoutput(self.check_local_path_cmd.format(variable=self.path_variable_name))
        if status == 1:
            # error
            self._set_var(self.path_variable_name, '~{0}~'.format(self.ruby_path_key))
        elif status == 0:
            path = ''.join(re.compile("\s+").split(output.strip("\n").split("\n")[-1].strip(" "))[2:])
            if '%{0}%'.format(self.ruby_path_key) not in path:
                # path = '~{0}~;{1};'.format(self.ruby_path_key, path.replace('%', '~'))
                path = '%%{0}%%'.format(self.ruby_path_key)
                self._set_var(self.path_variable_name, path)

        print(status, output)


if __name__ == '__main__':
    v = VarSetter()
    # v.set_version('')
    v._make_path()
