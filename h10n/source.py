import os
import inspect

import json
try:
    # Include YAML support if it available
    import yaml
except ImportError:
    yaml = None


class DictSource(object):

    def __init__(self, data):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0]).__name__
        line = frame[2]
        self.name = '{0}:{1}'.format(module, line)
        self.data = data

    def __getitem__(self, locale):
        return self.data[locale]


class FileSource(object):

    parsers = {'.json': json.loads}
    if yaml:
        parsers['.yaml'] = parsers['.yml'] = yaml.load

    def __init__(self, *dirs):
        self.dirs = dirs
        self.name = None

    def __getitem__(self, locale):
        return self._load_translations(locale)

    def _load_translations(self, locale):
        for dir in self.dirs:
            locale_path = os.path.join(dir, locale)
            if os.path.isdir(locale_path):
                for path, subdirs, files in os.walk(locale_path):
                    # Load translations from files
                    for name in files:
                        ext = os.path.splitext(name)[1]
                        if ext not in self.parsers:
                            continue
                        file_path = os.path.join(path, name)
                        parser = self.parsers[ext]
                        for item in self._load_file(file_path, parser):
                            yield item
                    # Skip hidden directories
                    for name in subdirs:
                        if name.startswith('.'):
                            subdirs.remove(name)
            else:
                for ext, parser in self.parsers.iteritems():
                    file_path = locale_path + ext
                    if os.path.isfile(file_path):
                        for item in self._load_file(file_path, parser):
                            yield item

    def _load_file(self, path, parser):
        with open(path) as f:
            self.name = f
            data = parser(f.read())
            for item in data:
                yield item
