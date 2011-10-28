from nose import tools
import os

from h10n.source import YAMLSource

data_path = os.path.join(os.path.dirname(__file__), 'data')

def yaml_test():
    """ YAML Source test """
    path = os.path.join(data_path, 'test.yaml')
    source = YAMLSource(path)
    tools.eq_(source, {'message_1': {'msg': 'Message 1'},
                       'message_2': {'msg': 'Message 2'}})
