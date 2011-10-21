""" The tests for Message Module """

from nose import tools

from h10n.server.message import Message


class Helpers(object):
    """ An example of Helper Namespace """

    def pluralize(self, locale, count):
        return 0 if count == 1 else 1

    def add(self, locale, left, right):
        return left + right

    def mul(self, locale, left, right):
        return left * right

    def swap_args(self, locale, first, second):
        return second, first

    def print_args(self, locale, *args, **kwargs):
        keys = kwargs.keys()
        keys.sort()
        result = [repr(arg) for arg in args]
        result.extend('{0}={1}'.format(k, repr(kwargs[k])) for k in keys)
        return ', '.join(result)

class Locale(object):
    """ A fake Locale """

    def __init__(self, name):
        self.helpers = Helpers()
        self.name = name

    def get_helper(self, name):
        """ Returns helper method by name """
        return getattr(self.helpers, name)


def setup():
    global prototype
    locale = Locale('en-US')
    prototype = Message(locale)


def format_test():
    """ The Message Module: Format Test """
    # Simple format
    definition = {
        'id': 'test',
        'msg': 'Message'
    }
    message = prototype.clone(**definition)
    result = message.format()
    tools.eq_(result, 'Message')

    # Format using default parameters and passed ones
    definition = {
        'id': 'test',
        'defaults': {'a': 1, 'b': 2},
        'msg': 'Message {a} {b} {c}'
    }
    message = prototype.clone(**definition)
    result = message.format(b=20, c=30)
    tools.eq_(result, 'Message 1 20 30')

    # Format using key and filters
    definition = {
        'id': 'test',
        'defaults': {'count': 1},
        'filters': [
            ('pluralize', '{count}', '{plural_form}'),
        ],
        'key': '{plural_form}',
        'msg': {
            '0': '{count} message',
            '1': '{count} messages',
        }
    }
    message = prototype.clone(**definition)
    result = message.format(count=2)
    tools.eq_(result, '2 messages')


def extension_test():
    """ The Message Module: Filters Extension Test """
    definition = {
        'id': 'parent',
        'filters': [
            ('add', ['{a}', '{b}'], '{a}'),
        ],
        'msg': '{a}'
    }
    parent = prototype.clone(**definition)

    # Implicit extension of filters
    definition = {
        'id': 'test',
        'filters': [
            ('mul', ['{a}', '{b}'], '{a}'),
        ],
        'msg': '{a}'
    }
    message = parent.clone(**definition)
    result = message.format(a=3, b=3)
    tools.eq_(result, '18')

    # Explicit extension of filters
    definition = {
        'id': 'test',
        'filters': [
            ('mul', ['{a}', '{b}'], '{a}'),
            '__prototype__',
        ],
        'msg': '{a}'
    }
    message = parent.clone(**definition)
    result = message.format(a=3, b=3)
    tools.eq_(result, '12')

    # Overriding prototype's filters
    definition = {
        'id': 'test',
        'filters': [
            '__no_prototype__',
            ('mul', ['{a}', '{b}'], '{a}'),
        ],
        'msg': '{a}'
    }
    message = parent.clone(**definition)
    result = message.format(a=3, b=3)
    tools.eq_(result, '9')


def compilation_test():
    """ The Message Module: Filter Compilation Test """

    # Process multiple filter result
    definition = {
        'id': 'test',
        'filters': [
            ('swap_args', ['{a}', '{b}'], ['{a}', '{b}']),
        ],
        'msg': '{a} {b}'
    }
    message = prototype.clone(**definition)
    result = message.format(a=1, b=2)
    tools.eq_(result, '2 1')

    # Passing to filter positional arguments
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', ['{a}', '{b}'], '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format(a=1, b=2)
    tools.eq_(result, '1, 2')

    # Passing to filter single postional argument
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', '{a}', '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format(a=1)
    tools.eq_(result, '1')

    # Passing to filter no arguments
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', [], '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format()
    tools.eq_(result, '')

    # Passing to filter keyword arguments
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', {'a': '{a}', 'b': '{b}'}, '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format(a=1, b=2)
    tools.eq_(result, 'a=1, b=2')

    # Passing to filter keyword and positional arguments
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', {'*': [1, 2], 'a': '{a}', 'b': '{b}'}, '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format(a=1, b=2)
    tools.eq_(result, '1, 2, a=1, b=2')

    # Passing to filter keyword arguments and single positional one
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', {'*': 1, 'a': '{a}', 'b': '{b}'}, '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format(a=1, b=2)
    tools.eq_(result, '1, a=1, b=2')

    # Passing to filter primitive datatypes via arguments
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', [None, False, True, 'string'], '{result}'),
        ],
        'msg': '{result}'
    }
    message = prototype.clone(**definition)
    result = message.format()
    tools.eq_(result, "None, False, True, 'string'")

    # Passing to filter value of argument's attribute """
    definition = {
        'id': 'test',
        'filters': [
            ('print_args', '{locale}.name', '{result}'),
        ],
        'msg': 'Locale is {result}'
    }
    message = prototype.clone(**definition)
    result = message.format(locale=message.locale)
    tools.eq_(result, "Locale is 'en-US'")


def exception_test():
    """ The Message Module: Exception Test """
    # Process invalid defaults
    definition = {
        'id': 'test',
        'defaults': 100,
        'msg': 'Message'
    }
    debug = None
    try:
        message = prototype.clone(**definition)
    except Exception, e:
        debug = e.args[-1]
    tools.eq_(debug, '<Message: en-US.test>')

    # Process invalid filters
    definition = {
        'id': 'test',
        'filters': [('invalid', [], '{result}')],
        'msg': 'Message'
    }
    debug = None
    try:
        message = prototype.clone(**definition)
    except Exception, e:
        debug = e.args[-2:]
    tools.eq_(debug, ('<Filter: invalid>', '<Message: en-US.test>'))
