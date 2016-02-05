import os
import subprocess

from core.lib import utils


class VarSetter(object):
    def __init__(self):
        self.ruby_path_key = 'RUBY'
        self.bat_path = utils.app_path('core/environment')
        self.bat_name = 'setenv.bat'
        self.bat_file = os.path.join(self.bat_path, self.bat_name)

    def set_version(self, path):
        self._make_path()
        self._set_var(self.ruby_path_key, path)

    def _set_var(self, key, value):
        self._create_bat(key, value)
        status, output = subprocess.getstatusoutput(self.bat_file)
        print(status)
        print(output)

    def _create_bat(self, key, value):
        command = 'setx %s %s\n' % (key, value)
        print(command)
        open(self.bat_file, 'w').write(command)

    def _make_path(self):
        return
        # fixme: path escape problems for paths with spaces
        if os.environ.get(self.ruby_path_key) is None:
            self._set_var('PATH', '"{0};%{1}%;"'.format(
                os.environ.get('PATH').replace('"', '\\"').rstrip(';'), self.ruby_path_key
            ))


if __name__ == '__main__':
    v = VarSetter()
    v.set_version('')
