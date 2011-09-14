""" Filter Compiler

An utility module that provides functions to compile filters.
Is used by ``h10n.translator.Translation``.
"""

def compile_chain(helpers, filters):
    """ Compile chain of filters

    Arguments:
        helpers
            Helper Manager instance
        filters
            An iterable that contain filter definitions. Definition is tuple
            or list of three items: filter method name, input map,
            and output map.

    Yields compiled filter.
    """
    for method_name, in_, out_ in filters:
        method_name = method_name.split('.')
        method = helpers
        for name in method_name:
            method = getattr(method, name)
        yield compile_filter(method, in_, out_)

def compile_filter(method, in_, out_):
    """ Compile filter

    Returns callable, that accept single dictionary argument ``kw``.
    This callable calls ``method`` with parameters extracted from ``kw``
    according to input map ``in_``, and put result into ``kw``
    according to output map ``out_``.  See ``h10n._compiler._template``
    for details.

    Arguments:
        method
            Filter method to call.
        in_
            Input map.  Can be list-like object, dict-like object, or any
            primitive data type.  Primitive data type always converts to
            list.  List-like map means to put all parameters as positional
            ones.  Dict-like map means to put parameters as keyword ones.
            Dict-like map can contain list-like under the key ``*``.
            This means to put positional parameters before keyword ones.
            Map can contain placeholders as string in format ``{name}``.
            This means to extract value from ``kw``.
            See ``h10n._compiler._map`` and ``h10n._compiler._value`` docstrings
            for more detailed information about maps.
        out_
            Output map.  Same is input map, but can contain only list or string.
            All items must be in form ``{name}``.

    Returns compiled filter

    See ``h10n.tests.compiler_test`` for example.
    """
    code = _template.format(in_=_map(in_), out_=_map(out_))
    exec code in locals()
    #noinspection PyUnresolvedReferences
    return f


_template = 'def f(kw): ({out_}) = method({in_})'

def _map(map):
    """ Map Converter

    Converts map into Python code fragment, that will be used
    in ``h10n._compiler._template`` by ``h10n._compiler.compile`` to construct
    source code of filter.

    Example::
        >>> _map({'*': [1, '{a}', '{b}.b'], 'c': '{c}["c"]'})
        '1, kw["a"], kw["b"].b, c=kw["c"]["c"]'
    """
    if hasattr(map, 'keys'):
        # When map is dict-like object
        kw = dict(map)
        args = kw.pop('*', [])
    elif hasattr(map, '__iter__'):
        # When map is iterable object without keys (list-like)
        args = list(map)
        kw = {}
    else:
        # When map is not iterable
        args = [map]
        kw = {}
    result = [_value(arg) for arg in args]
    result.extend('{0}={1}'.format(name, _value(arg))
                  for name, arg in kw.iteritems())
    result = ', '.join(result)
    return result

def _value(value):
    """ Value converter

    Converts value into Python code fragment, that will be used to construct
    map source code.

    Example::
        >>> _value(1)
        '1'
        >>> _value('abc')
        "'abc'"
        >>> _value('{abc}')
        'kw["abc"]'
    """
    if isinstance(value, basestring) and '{' in value:
        value = value.replace('{', 'kw["').replace('}', '"]')
    else:
        value = repr(value)
    return value


if __name__ == '__main__':
    from doctest import testmod
    testmod()
