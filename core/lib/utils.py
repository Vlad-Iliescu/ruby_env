import os
import re

VERSION_RE = re.compile('\d\.\d\.\d')
NORMALIZE_RE = re.compile('[-\(\).]+')


def ruby_version_from_string(raw_version):
    return VERSION_RE.findall(raw_version)[0]


def normalize_version(raw_version, normalize_char='_'):
    normalized = NORMALIZE_RE.sub(' ', raw_version)
    normalized = re.sub('(?:^\s+|\s+$)', '', normalized)
    normalized = re.sub('\s+', normalize_char, normalized)
    return normalized.lower()


def app_path(path=None):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)
            ),
            '..',
            '..',
            path or ''
        )
    )
