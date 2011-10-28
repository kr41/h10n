from nose import tools

from h10n.util import keep_context
from h10n.util import NamedObject


class Item(NamedObject):

    def __init__(self, name):
        self.name = name

    @keep_context
    def error_method(self):
        raise Exception('Test context')

class Container(NamedObject):

    def __init__(self, name, item):
        self.name = name
        self.item = item

    @keep_context
    def test_context(self):
        self.item.error_method()

    @keep_context
    def test_duplicate(self):
        self.error_method()

    @keep_context
    def error_method(self):
        raise Exception('Test duplicate')


def context_test():
    """ Exception Context Test """
    container = Container(1, Item(1))

    # Context test
    context = None
    try:
        container.test_context()
    except Exception, e:
        context = e.args[-1]
    tools.eq_(repr(context), '<ExceptionContext: [<Container: 1>, <Item: 1>]>')

    # Duplicate context test
    context = None
    try:
        container.test_duplicate()
    except Exception, e:
        context = e.args[-1]
    tools.eq_(repr(context), '<ExceptionContext: [<Container: 1>]>')
