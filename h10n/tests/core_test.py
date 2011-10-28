from nose import tools

from h10n.core import Root


def setup():
    global root

    # Define Localization Server
    root = Root(
        'test',
        {
            'en-US': {
                'format_test':{
                    'messages': {
                        '__helpers__': """
                            from h10n.tests.helpers import *
                        """,
                        'simple': 'Simple Message',
                        'params': {
                            'defaults': {'a': 1, 'b': 2},
                            'msg': 'Parametrized Message with params: '
                                   'a={a} b={b} c={c}'
                        },
                        'key_and_filter': {
                            'defaults': {'count': 1},
                            'filter': """
                                $plural_form = pluralize($count)
                            """,
                            'key': '{plural_form}',
                            'msg': {
                                '0': '{count} message',
                                '1': '{count} messages',
                            }
                        }
                    }
                },
                'helpers_test': {
                    'messages': {
                        '__helpers__': """
                            from h10n.tests.helpers import *
                        """,
                        'base': {
                            'filter': """
                                $a = add($a, $b)
                            """,
                            'msg': '{a}'
                        },
                        'extension': {
                            'prototype': 'helpers_test.base',
                            'filter': """
                                $a = mul($a, $b)
                                __prototype__
                            """,
                            'msg': '{a}'
                        },
                        'generic': {
                            'filter': """
                                $result = generic.message(
                                    __locale__,
                                    'helpers_test.base', a=1, b=2
                                )
                            """,
                            'msg': '{result}'
                        }
                    }
                }
            }
        }
    )


def format_test():
    """ Message Format Test """
    # Simple format
    result = root['en-US.format_test.simple'].format()
    tools.eq_(result, 'Simple Message')

    # Format using default parameters and passed ones
    result = root['en-US.format_test.params'].format(b=20, c=30)
    tools.eq_(result, 'Parametrized Message with params: a=1 b=20 c=30')

    # Format using key and filters
    result = root['en-US.format_test.key_and_filter'].format(count=2)
    tools.eq_(result, '2 messages')


def extension_test():
    """ Message Filters Extension Test """
    # Extension of filters
    result = root['en-US.helpers_test.extension'].format(a=3, b=3)
    tools.eq_(result, '12')

    # Using generic (built-in) helpers
    result = root['en-US.helpers_test.generic'].format()
    tools.eq_(result, '3')
