import os
from nose import tools

from h10n.source import scanner, scan_path, scan_asset
from h10n.source import YAMLSource

path = os.path.join(os.path.dirname(__file__), 'assets')
check = {
    'en-US': {
        'source': {
            'factory': YAMLSource,
            'path': os.path.join(path, 'en-US', 'source.yaml')
        },
        'nested.source': {
            'factory': YAMLSource,
            'path': os.path.join(path, 'en-US', 'nested', 'source.yaml')
        },
    }
}

def scan_path_test():
    result = scan_path(path)
    tools.eq_(result, check)

def scan_asset_test():
    result = scan_asset('h10n.tests.unit_tests.source_test:assets')
    tools.eq_(result, check)

def scanner_test():
    result = list(scanner(['path://{0}'.format(path),
                           'asset://h10n.tests.unit_tests.source_test:assets']))
    tools.eq_(result[0], check)
    tools.eq_(result[1], check)

