from nose import tools

from h10n.core import Catalog, Message


def compile_message_test():
    prototype = Message(msg='Prototype')
    fake_locale = {'other_catalog:prototype': prototype}
    catalog = Catalog('Test', fake_locale, {
        'short': 'Short specification of message',
        'full': {
            'msg': 'Full specification of message'
        },
        'from_prototype': {
            'prototype': 'other_catalog:prototype'
        }
    })
    tools.eq_(catalog['short'].format(), 'Short specification of message')
    tools.eq_(catalog['full'].format(), 'Full specification of message')
    tools.eq_(catalog['from_prototype'].format(), 'Prototype')
    tools.eq_(catalog['from_prototype'].prototype, prototype)

def custom_source_test():
    class SourceFactory(dict):
        log = []
        def __getitem__(self, key):
            self.log.append('get {0}'.format(key))
            return dict.__getitem__(self, key)
        def __setitem__(self, key, value):
            self.log.append('set {0}: {1}'.format(key, type(value)))
            return dict.__setitem__(self, key, value)
    catalog = Catalog('Test', None, {
        'factory': SourceFactory,
        'msg': 'Message',
    })
    catalog['msg']
    tools.eq_(SourceFactory.log, ['get msg',
                                  "set msg: <class 'h10n.core.Message'>"])

def factory_keyword_test():
    catalog = Catalog('Test', None, {
        'factory': 'Is not callable == Regular message',
    })
    tools.eq_(catalog['factory'].format(), 'Is not callable == Regular message')
