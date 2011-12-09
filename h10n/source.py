import os
import re
import pkg_resources
import yaml
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader


class YAMLSource(dict):

    def __init__(self, path):
        with open(path) as f:
            self.update(yaml.load(f, Loader=YAMLLoader))


# TODO: Replace it by scaning entry points
file_sources = {
    '.yaml': YAMLSource,
    '.yml': YAMLSource,
}

def scan_path(base_path, prefix=''):
    if not os.path.isabs(base_path):
        # Resolve ``base_path`` as ``package.name:directory/to/scan``
        if ':' in base_path:
            package, dir = base_path.split(':')
        else:
            package, dir = base_path, ''
        base_path = pkg_resources.resource_filename(package, dir)
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
                file_path = os.path.join(path, name)
                full_name = os.path.relpath(file_path, locale_path)
                name, ext = os.path.splitext(full_name)
                ext = ext.lower()
                if ext not in file_sources:
                    logger.info('Unsupported file type "{0}"; skipped'.
                                format(file_path))
                    continue
                name = prefix + name.replace(os.path.sep, '.')
                locale[name] = {
                    'factory': file_sources[ext],
                    'path': file_path,
                }
            # Skip directories which names starts with '.' or '_'
            for name in dirs[:]:
                if name[0] in ('.', '_'):
                    dirs.remove(name)
    return result
