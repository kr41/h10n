""" The tests for Filter Module """

from nose import tools

from h10n.server.filter import FilterChain


class Helpers(object):
    """ An example Helper Namespace """

    def add(self, left, right):
        return left + right

    def mul(self, left, right):
        return left * right

    def swap(self, left, right):
        return (right, left)

    def format_list(self, *args, **kwargs):
        before = kwargs.get('before', '[')
        after =  kwargs.get('after', ']')
        delimiter = kwargs.get('delimiter', ', ')
        return before + delimiter.join(str(a) for a in args) + after


def setup():
    global prototype
    helpers = Helpers()
    prototype = FilterChain(helpers)


def positional_args_test():
    """ Passing positional arguments to Helper Method """
    params = {'a': 1, 'b': 2}

    definitions = [
        ('add', ['{a}', '{b}'], '{a}'),
    ]
    filter = prototype.clone(definitions)
    filter.apply(params)

    tools.eq_(params, {'a': 3, 'b': 2})

def keyword_args_test():
    """ Passing key-word arguments to Helper Method """
    params = {'a': 1, 'b': 2}

    definitions = [
        ('add', {'left': '{a}', 'right': '{b}'}, '{a}'),
    ]
    filter = prototype.clone(definitions)
    filter.apply(params)

    tools.eq_(params, {'a': 3, 'b': 2})

def as_is_args_test():
    """ Passing arguments to Helper Method as-is from Filter Definition """
    params = {}

    definitions = [
        ('add', [1, 2], '{a}'),
    ]
    filter = prototype.clone(definitions)
    filter.apply(params)

    tools.eq_(params, {'a': 3})

def mixed_args_test():
    """ Passing arguments in mixed style to Helper Method """
    params = {'a': 1, 'b': 2}

    definitions = [
        (
            'format_list',
            {'*': ['{a}', '{b}'], 'before': '(', 'after': ')'},
            '{list}'
        ),
    ]
    filter = prototype.clone(definitions)
    filter.apply(params)

    tools.eq_(params, {'a': 1, 'b': 2, 'list': '(1, 2)'})

def mixed_args_test_marginal_case():
    """ Passing arguments in mixed style to Helper Method (marginal case) """
    params = {'a': 1}

    definitions = [
        (
            'format_list',
            {'*': '{a}', 'before': '(', 'after': ')'},
            '{list}'
        ),
    ]
    filter = prototype.clone(definitions)
    filter.apply(params)

    tools.eq_(params, {'a': 1, 'list': '(1)'})

def multiple_result_test():
    """ Getting multiple result from Helper Method """
    params = {'a': 1, 'b': 2}

    definitions = [
        ('swap', ['{a}', '{b}'], ['{a}', '{b}']),
    ]
    filter = prototype.clone(definitions)
    filter.apply(params)

    tools.eq_(params, {'a': 2, 'b': 1})

def implicit_extend_test():
    """ Implicit extension of Prototype's Filter Chain """
    params = {'a': 1, 'b': 2, 'c': 3}

    definitions = [
        ('add', ['{a}', '{b}'], '{a}'),
    ]
    parent = prototype.clone(definitions)

    definitions = [
        ('mul', ['{a}', '{c}'], '{a}'),
    ]
    filter = parent.clone(definitions)
    filter.apply(params)

    # (1 + 2) * 3 == 9
    tools.eq_(params, {'a': 9, 'b': 2, 'c': 3})

def explicit_extend_test():
    """ Explicit extension of Prototype's Filter Chain """
    params = {'a': 1, 'b': 2, 'c': 3}

    definitions = [
        ('add', ['{a}', '{b}'], '{a}'),
    ]
    parent = prototype.clone(definitions)

    definitions = [
        ('mul', ['{a}', '{c}'], '{a}'),
        '__prototype__'
    ]
    filter = parent.clone(definitions)
    filter.apply(params)

    # 1 * 3 + 2 == 5
    tools.eq_(params, {'a': 5, 'b': 2, 'c': 3})

def override_test():
    """ Overriding Prototype's Filter Chain """
    params = {'a': 1, 'b': 2, 'c': 3}

    definitions = [
        ('add', ['{a}', '{b}'], '{a}'),
    ]
    parent = prototype.clone(definitions)

    definitions = [
        '__no_prototype__',
        ('mul', ['{a}', '{c}'], '{a}'),
    ]
    filter = parent.clone(definitions)
    filter.apply(params)

    # 1 * 3 == 3
    tools.eq_(params, {'a': 3, 'b': 2, 'c': 3})
