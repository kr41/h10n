from nose import tools

from h10n.util import Namespace

def regular_extend_test():
    obj = Namespace()
    # Extend by regular dict
    obj.extend({'a': 1, 'b.c': 2})
    tools.eq_(obj.a, 1)
    tools.eq_(obj.b.c, 2)
    # Extend by Namespace instance
    obj.extend(Namespace().extend({'a': 2, 'b.d': 3}))
    tools.eq_(obj.a, 2)
    tools.eq_(obj.b.c, 2)
    tools.eq_(obj.b.d, 3)

@tools.raises(AttributeError)
def invalid_extend_test():
    obj = Namespace().extend({'_a': 1})
    obj._a

@tools.raises(AttributeError)
def extend_with_skips_test():
    obj = Namespace().extend({'a': 1}, ('a'))
    obj.a

def getter_test():
    obj_1 = object()
    obj_2 = object()
    obj = Namespace().extend({'a': obj_1, 'b.c': obj_2})
    # Regular get
    tools.eq_(obj.get('a'), obj_1)
    tools.eq_(obj.get('c'), None)
    tools.eq_(obj.get('c', obj_2), obj_2)
    # Get using dot notation
    tools.eq_(obj.get('b.c'), obj_2)
    tools.eq_(obj.get('b.d'), None)
    tools.eq_(obj.get('b.d', obj_2), obj_2)
    # Nested get
    tools.eq_(obj.get('b').get('c'), obj_2)
    tools.eq_(obj.get('b').get('d'), None)
    tools.eq_(obj.get('b').get('d', obj_2), obj_2)

def strict_getter_test():
    obj_1 = object()
    obj_2 = object()
    obj = Namespace().extend({'a': obj_1, 'b.c': obj_2})
    tools.eq_(obj['a'], obj_1)
    tools.eq_(obj['b.c'], obj_2)
    tools.eq_(obj['b']['c'], obj_2)

@tools.raises(KeyError)
def strict_getter_exception_test():
    obj = Namespace()
    obj['a']
