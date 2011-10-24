import json
import yaml
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader
import dbm


#
# On-start-up Sources
###############################################################################

class OnStartUpSource(object):

    strategy = 'on_start_up'

    def __iter__(self):
        for item in self.data:
            yield item


class JSONSource(OnStartUpSource):

    def __init__(self, path):
        with open(path) as f:
            data = json.load(f, loader=YAMLLoader)


class YAMLSource(OnStartUpSource):

    def __init__(self, path):
        with open(path) as f:
            data = yaml.load()


#
# On-demand Sources
###############################################################################

class OnDemandSource(object):

    strategy = 'on_demand'


class DBMSource(OnDemandSource):

    def __init__(self, path):
        data = dbm.open(path)

    def __getitem__(self, id):
        return json.loads(self.data[id])
