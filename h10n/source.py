import os
import re
import pkg_resources
import yaml
import logging
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader


logger = logging.getLogger(__name__)

class YAMLSource(dict):

    def __init__(self, path):
        with open(path) as f:
            self.update(yaml.load(f, Loader=YAMLLoader))


def scanner(uri_list):
    for uri in uri_list:
        protocol, id = uri.split('://')
        try:
            yield scanners[protocol](id)
        except KeyError:
            raise ValueError('Unknown scanner "{0}"'.format(protocol))

def scan_py(spec):
    if ':' not in spec:
        spec += ':locales'
    return pkg_resources.EntryPoint.parse('x={0}'.format(spec)).load(False)

def scan_asset(spec):
    if ':' in spec:
        package, dir = spec.split(':')
    else:
        package, dir = spec, ''
    path = pkg_resources.resource_filename(package, dir)
    return scan_path(path)

def scan_path(base_path):
    if not os.path.isdir(base_path):
        raise ValueError("Can't to scan path {0}".format(base_path))
    result = {}
    locale_pattern = re.compile(r'[a-z]{2}\-[A-Z]{2}')
    for locale_name in os.listdir(base_path):
        locale_path = os.path.join(base_path, locale_name)
        if not (os.path.isdir(locale_path) and
                locale_pattern.match(locale_name)):
            continue
        locale = result[locale_name] = {}
        for path, dirs, files in os.walk(locale_path):
            for name in files:
                if name[0] in ('.', '_'):
                    continue
                file_path = os.path.join(path, name)
                full_name = os.path.relpath(file_path, locale_path)
                name, ext = os.path.splitext(full_name)
                ext = ext.lower()
                if ext not in file_sources:
                    logger.info('Unsupported file type "{0}"; skipped'.
                                format(file_path))
                    continue
                name = name.replace(os.path.sep, '.')
                locale[name] = {
                    'factory': file_sources[ext],
                    'path': file_path,
                }
            # Skip directories which names starts with '.' or '_'
            for name in dirs[:]:
                if name[0] in ('.', '_'):
                    dirs.remove(name)
    return result


file_sources = {}
for entry_point in pkg_resources.iter_entry_points('h10n.source.file'):
    file_sources[entry_point.name] = entry_point.load()

scanners = {}
for entry_point in pkg_resources.iter_entry_points('h10n.scanner'):
    scanners[entry_point.name] = entry_point.load()
