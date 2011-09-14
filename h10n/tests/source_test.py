""" The tests for Translation Sources """

import os
from nose import tools

from h10n.source import DictSource, FileSource
from h10n.tests import data


data_dir = os.path.join(os.path.dirname(__file__), 'data/filesource')

def test_dirs():
    """ ``FileSource`` based on locale directories """
    source = FileSource(os.path.join(data_dir, 'test_dirs'))
    tools.eq_(list(source['en']), data.simple_source['en'])
    tools.eq_(list(source['ru']), data.simple_source['ru'])

def test_files():
    """ ``FileSource`` based on locale files """
    source = FileSource(os.path.join(data_dir, 'test_files'))
    tools.eq_(list(source['en']), data.simple_source['en'])
    tools.eq_(list(source['ru']), data.simple_source['ru'])

def test_source_name():
    """ Name detection of ``DictSource`` """
    source = DictSource({})
    tools.ok_(source.name.startswith(__name__))
