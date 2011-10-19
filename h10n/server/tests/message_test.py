""" The tests for Message Module """

from nose import tools

from h10n.message import Message


class Helpers(object):
    """ An example Helper Namespace """

    def pluralize(self, count):
        return 0 if count == 1 else 1

class Locale(object):
    """ A Fake Locale """

    def __init__(self):
        self.helpers = Helpers()


def setup():
    global prototype
    locale = Locale()
    prototype = Message(locale)


def simple_format_test():
    """ Simple format """
    definition = {
        'msg': "Message"
    }
    message = prototype.clone(**definition)
    result = message.format()
    tools.eq_(result, "Message")

def passing_params_test():
    """ Passing parameters to formatter """
    definition = {
        'msg': "Message {a} {b}"
    }
    message = prototype.clone(**definition)
    result = message.format(a=1, b=2)
    tools.eq_(result, "Message 1 2")

def default_params_test():
    """ Format using default parameters """
    definition = {
        'defaults': {'a': 1, 'b': 2},
        'msg': "Message {a} {b}"
    }
    message = prototype.clone(**definition)
    result = message.format(a=2)
    tools.eq_(result, "Message 2 2")

def filter_and_key_test():
    """ Format using key and filters """
    definition = {
        'defaults': {'count': 1},
        'filters': [
            ('pluralize', '{count}', '{plural_form}'),
        ],
        'key': '{plural_form}',
        'msg': {
            '0': "{count} message",
            '1': "{count} messages",
        }
    }
    message = prototype.clone(**definition)
    result = message.format()
    tools.eq_(result, "1 message")
