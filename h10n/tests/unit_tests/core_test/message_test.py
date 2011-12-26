from nose import tools

from h10n.core import Message


def simple_test():
    msg = Message(msg='Test Message')
    tools.eq_(msg.format(), 'Test Message')

def format_test():
    msg = Message(msg='a={a}, b={b}, c={c}', defaults={'a': 1, 'b': 2})
    tools.eq_(msg.format(b=3, c=3), 'a=1, b=3, c=3')

def properties_test():
    msg = Message(property_1=1)
    tools.eq_(msg.property_1, 1)

def key_test():
    msg = Message(msg={'1': 'key=1', '2': 'key=2'}, key='{key}')
    tools.eq_(msg.format(key=1), 'key=1')
    tools.eq_(msg.format(key=2), 'key=2')

def filter_test():
    msg = Message(msg='{b}', filter='$b = $a * self.factor', factor=2)
    tools.eq_(msg.format(a=10), '20')

def prototype_key_and_msg_test():
    prototype = Message(msg={'1': 'key=1', '2': 'key=2'}, key='{key}')
    msg = Message(prototype=prototype)
    tools.eq_(msg.format(key=1), 'key=1')
    tools.eq_(msg.format(key=2), 'key=2')

def prototype_defaults_test():
    prototype = Message(defaults={'a': 1, 'b': 2})
    msg = Message(prototype=prototype, defaults={'b': 3, 'c': 3},
                  msg='a={a}, b={b}, c={c}')
    tools.eq_(msg.format(), 'a=1, b=3, c=3')

def prototype_properties_test():
    prototype = Message(a=1, b=2)
    msg = Message(prototype=prototype, b=3, c=3)
    tools.eq_(msg.a, 1)
    tools.eq_(msg.b, 3)
    tools.eq_(msg.c, 3)

def prototype_filter_default_test():
    prototype = Message(filter='$b = $a * self.factor', factor=2)
    msg = Message(prototype=prototype, msg='{b}', factor=3)
    tools.eq_(msg.format(a=10), '30')

def prototype_filter_extend_test():
    prototype = Message(filter='$b = $a * self.factor', factor=2)
    msg = Message(prototype=prototype, msg='{b}', factor=3, filter="""
        __prototype__
        $b += $c
    """)
    tools.eq_(msg.format(a=10, c=3), '33')
