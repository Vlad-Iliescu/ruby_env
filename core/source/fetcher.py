import os
import requests

from core.lib import utils
from core.source.handler import Handler

try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO


class Fetcher(object):
    def __init__(self):
        self.url = 'http://rubyinstaller.org/downloads/archives'
        self.contents = None
        self.handler = Handler()

    def get_available_versions(self):
        self.__fetch()
        self.__parse()
        return self.handler.versions

    def get_version(self, version, url, name=None):
        req = requests.get(url)
        if req.status_code == 200:
            folder = utils.ruby_version_from_string(version)
            filename = name or utils.normalize_version(version)
            path = utils.app_path('dist/{0}/{1}.7z'.format(folder, filename))
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            open(path, 'wb').write(req.content)
            return path
        raise RuntimeError('Error downloading %s' % url)

    def __fetch(self):
        req = requests.get(self.url)
        if req.status_code == 200:
            file = StringIO()
            file.write(req.content)
            file.seek(0)

            self.contents = file
        else:
            raise IOError('Cannot connect to RubyInstaller.')

    def __parse(self):
        parser = self.handler.get_parser()
        parser.parse(self.contents)


if __name__ == '__main__':
    fetcher = Fetcher().get_available_versions()
    Fetcher().get_version(
        'Ruby 2.0.0-p247 (x64)',
        'http://dl.bintray.com/oneclick/rubyinstaller/ruby-2.0.0-p481-x64-mingw32.7z'
    )
