import os
import shutil
import subprocess

from core.archive import Extractor
from core.database import RecordNotFound
from core.source import Fetcher
from app import Version, Available
from core.lib import utils
from future.utils import iteritems

__all__ = ['Application']


class Application(object):
    def __init__(self, args):
        self.rm_cmd = 'rd /s /q {path}'

    def get_available_versions(self):
        fetcher = Fetcher()
        versions = fetcher.get_available_versions()
        if versions:
            Available.truncate()
            for (version, url) in iteritems(versions):
                available = Available()
                available.full_version = version
                available.version_name = utils.normalize_version(version.lower())
                available.ruby_version = utils.ruby_version_from_string(version)
                available.url = url
                available.save()

    def list_available_versions(self):
        return Available.all()

    def get_installed(self):
        return Version.all()

    def install_version(self, version, name=None):
        avail_version = Available.find_by('version_name', version.lower())
        name = name or avail_version.version_name
        try:
            installed = Version.find_by('name', name)
            if installed.ruby_version == avail_version.ruby_version:
                raise RuntimeError('A version with this name already exists "%s"' % name)
        except RecordNotFound:
            pass

        archive_path = self.fetch_version(avail_version, name)
        archive_folder = self.extract_version(archive_path, avail_version, name)
        os.remove(archive_path)

        new_version = Version()
        new_version.name = name
        new_version.version_name = avail_version.version_name
        new_version.ruby_version = avail_version.ruby_version
        new_version.full_version = avail_version.full_version
        new_version.folder = archive_folder
        new_version.save()

    def fetch_version(self, version, name):
        fetcher = Fetcher()
        return fetcher.get_version(version.full_version, version.url, name)

    def extract_version(self, archive_path, version, name):
        extractor = Extractor()
        archive_folder = extractor.get_archived_folder_name(archive_path)
        extractor.extract(archive_path, utils.app_path(os.path.join('dist', 'tmp')))
        destination = utils.app_path(os.path.join('dist', version.ruby_version, name))
        shutil.move(
            utils.app_path(os.path.join('dist', 'tmp', archive_folder)),
            destination
        )
        os.chmod(destination, 0o777)
        return destination

    def remove_version(self, version):
        installed = Version.find_by('name', version)
        installed.remove()
        subprocess.getstatusoutput(self.rm_cmd.format(path=installed.folder))


if __name__ == '__main__':
    app = Application({})
    # app.get_available_versions()
    # list_ = app.list_available_versions()
    app.install_version('ruby_2_1_6', 'ruby216-2')
    list_ = app.get_installed()
    # app.remove_version('ruby216-2')
    pass
