from nose import tools

from h10n.exception import keep_context


class Item(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Item: {0}>'.format(self.name)

    @keep_context()
    def method(self):
        raise Exception('Test context')

class Container(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Container: {0}>'.format(self.name)

    @keep_context()
    def method(self):
        Item(1).method()


def context_test():
    container = Container(1)

    # Test implicit context
    context = None
    try:
        container.method()
    except Exception, e:
        context = e.args[-1]
    tools.eq_(repr(context), '<Context: [<Container: 1>, <Item: 1>]>')

    # Test explicit context
    @keep_context(context=container)
    def func():
        raise Exception('Test context')
    context = None
    try:
        func()
    except Exception, e:
        context = e.args[-1]
    tools.eq_(repr(context), '<Context: [<Container: 1>]>')
