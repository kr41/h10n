from nose import tools

from h10n.core import Server


def setup():
    global server

    # Define helper functions
    def pluralize(locale, count):
        return 0 if count == 1 else 1

    def add(locale, left, right):
        return left + right

    def mul(locale, left, right):
        return left * right

    def swap_args(locale, first, second):
        return second, first

    def print_args(locale, *args, **kwargs):
        keys = kwargs.keys()
        keys.sort()
        result = [repr(arg) for arg in args]
        result.extend('{0}={1}'.format(k, repr(kwargs[k])) for k in keys)
        return ', '.join(result)

    # Define Localization Server
    server = Server(
        locales={
            'en-US': {
                'catalogs': {
                    'on_start_up':{
                        'strategy': 'on_start_up',
                        'source': [
                            {
                                'id': 'simple_test',
                                'msg': 'Simple Message',
                            },
                            {
                                'id': 'params_test',
                                'defaults': {'a': 1, 'b': 2},
                                'msg': 'Parametrized Message with params: '
                                       'a={a} b={b} c={c}'
                            },
                            {
                                'id': 'key_and_filters_test',
                                'defaults': {'count': 1},
                                'filters': [
                                    ('pluralize', '{count}', '{plural_form}'),
                                ],
                                'key': '{plural_form}',
                                'msg': {
                                    '0': '{count} message',
                                    '1': '{count} messages',
                                }
                            },
                            {
                                'id': 'extension_test',
                                'filters': [
                                    ('add', ['{a}', '{b}'], '{a}'),
                                ],
                                'msg': '{a}'
                            }
                        ]
                    },
                    'on_demand': {
                        'strategy': 'on_demand',
                        'source': {
                            'implicit_extension_test': {
                                'prototype': 'on_start_up.extension_test',
                                'filters': [
                                    ('mul', ['{a}', '{b}'], '{a}'),
                                ],
                                'msg': '{a}'
                            },
                            'explicit_extension_test': {
                                'prototype': 'on_start_up.extension_test',
                                'filters': [
                                    ('mul', ['{a}', '{b}'], '{a}'),
                                    '__prototype__',
                                ],
                                'msg': '{a}'
                            },
                            'override_test': {
                                'prototype': 'on_start_up.extension_test',
                                'filters': [
                                    '__no_prototype__',
                                    ('mul', ['{a}', '{b}'], '{a}'),
                                ],
                                'msg': '{a}'
                            },
                        }
                    },
                    'compilation_test': {
                        'strategy': 'on_demand',
                        'source': {
                            'multiple_result': {
                                'filters': [
                                    ('swap_args', ['{a}', '{b}'],
                                                  ['{a}', '{b}']),
                                ],
                                'msg': '{a} {b}'
                            },
                            'positional_args': {
                                'filters': [
                                    ('print_args', ['{a}', '{b}'], '{result}'),
                                ],
                                'msg': '{result}'
                            },
                            'single_arg': {
                                'filters': [
                                    ('print_args', '{a}', '{result}'),
                                ],
                                'msg': '{result}'
                            },
                            'no_arg': {
                                'filters': [
                                    ('print_args', [], '{result}'),
                                ],
                                'msg': '{result}'
                            },
                            'keyword_args': {
                                'filters': [
                                    ('print_args', {'a': '{a}', 'b': '{b}'},
                                                    '{result}'),
                                ],
                                'msg': '{result}'
                            },
                            'mixed_args': {
                                'filters': [
                                    (
                                        'print_args',
                                        {'*': [1, 2], 'a': '{a}', 'b': '{b}'},
                                        '{result}'
                                    ),
                                ],
                                'msg': '{result}'
                            },
                            'mixed_args_2': {
                                'filters': [
                                    (
                                        'print_args',
                                        {'*': 1, 'a': '{a}', 'b': '{b}'},
                                        '{result}'
                                    ),
                                ],
                                'msg': '{result}'
                            },
                            'primitives': {
                                'id': 'test',
                                'filters': [
                                    (
                                        'print_args',
                                        [None, False, True, 'string'],
                                        '{result}'
                                    ),
                                ],
                                'msg': '{result}'
                            },
                            'attribute': {
                                'filters': [
                                    ('print_args', '{locale}.name', '{result}'),
                                ],
                                'msg': 'Locale is {result}'
                            }
                        }
                    }
                },
                'helpers': {
                    'pluralize': pluralize,
                },
            }
        },
        helpers={
            'add': add,
            'mul': mul,
            'swap_args': swap_args,
            'print_args': print_args,
        }
    )


def format_test():
    """ Message Format Test """
    # Simple format
    result = server['en-US.on_start_up.simple_test'].format()
    tools.eq_(result, 'Simple Message')

    # Format using default parameters and passed ones
    result = server['en-US.on_start_up.params_test'].format(b=20, c=30)
    tools.eq_(result, 'Parametrized Message with params: a=1 b=20 c=30')

    # Format using key and filters
    result = server['en-US.on_start_up.key_and_filters_test'].format(count=2)
    tools.eq_(result, '2 messages')


def extension_test():
    """ Message Filters Extension Test """
    # Implicit extension of filters
    result = server['en-US.on_demand.implicit_extension_test'].format(a=3, b=3)
    tools.eq_(result, '18')

    # Explicit extension of filters
    result = server['en-US.on_demand.explicit_extension_test'].format(a=3, b=3)
    tools.eq_(result, '12')

    # Overriding prototype's filters
    result = server['en-US.on_demand.override_test'].format(a=3, b=3)
    tools.eq_(result, '9')


def compilation_test():
    """ Message Filter Compilation Test """

    # Process multiple filter result
    result = server['en-US.compilation_test.multiple_result'].format(a=1, b=2)
    tools.eq_(result, '2 1')

    # Passing to filter positional arguments
    result = server['en-US.compilation_test.positional_args'].format(a=1, b=2)
    tools.eq_(result, '1, 2')

    # Passing to filter single postional argument
    result = server['en-US.compilation_test.single_arg'].format(a=1)
    tools.eq_(result, '1')

    # Passing to filter no arguments
    result = server['en-US.compilation_test.no_arg'].format()
    tools.eq_(result, '')

    # Passing to filter keyword arguments
    result = server['en-US.compilation_test.keyword_args'].format(a=1, b=2)
    tools.eq_(result, 'a=1, b=2')

    # Passing to filter keyword and positional arguments
    result = server['en-US.compilation_test.mixed_args'].format(a=1, b=2)
    tools.eq_(result, '1, 2, a=1, b=2')

    # Passing to filter keyword arguments and single positional one
    result = server['en-US.compilation_test.mixed_args_2'].format(a=1, b=2)
    tools.eq_(result, '1, a=1, b=2')

    # Passing to filter primitive datatypes via arguments
    result = server['en-US.compilation_test.primitives'].format()
    tools.eq_(result, "None, False, True, 'string'")

    # Passing to filter value of argument's attribute """
    result = server['en-US.compilation_test.attribute'] \
        .format(locale=server['en-US'])
    tools.eq_(result, "Locale is 'en-US'")
