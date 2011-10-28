import yaml
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader


class YAMLSource(dict):

    def __init__(self, path):
        with open(path) as f:
            self.update(yaml.load(f, Loader=YAMLLoader))
