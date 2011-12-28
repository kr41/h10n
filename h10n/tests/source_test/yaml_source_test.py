import os
from nose import tools

from h10n.source import YAMLSource


def test():
    path = os.path.join(os.path.dirname(__file__), 'assets/en-US/source.yaml')
    source = YAMLSource(path)
    tools.eq_(source['message'], 'Message')
    tools.eq_(source.keys(), ['message'])

