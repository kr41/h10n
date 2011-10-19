""" Filter Module

Provides functional to build Filter Chains.

Filter Chain is utility object which prepares parameters before formatting
Localized Messages.

Filter is callable accepting single argument -- dictionary with parameters
to filter.  It extracts parameters from dictionary, passes them into Helper
Method and puts result back into dictionary.

Chains are represented by class ``FilterChain``.  Its constructor accepts single
argument -- Helper Namespace object.  Instance of this class is an empty
prototype which is cloned with extending and/or overriding original filters
using Filter Chain Definitions.

Filter Chain Definitions is list of rules which provides information on
prototype chain extension.  Each definition is tuple of three items: helper
method name, input map, output map.  Maps contain information on how to
extract parameters from Filter argument (dictionary) and put result back.
Filter Definition is used for Filter compilation.

Helper Method name is dotted Python name of Helper callable relative
to Helper Namespace.

Map could be presented by dictionary, list or any primitive data type (it will
be converted to list at compile time).  Each item of the Map will be passed
to Helper as is, except placeholders.  Placeholder is a string in format
"{name}".  It will be replaced by respective parameter from Filter argument.
See ``h10n.filter._compile`` doc-string for details.

Also, the List of Definitions may contain special directives "__no_prototype__"
and "__prototype__".  First one is instruction to override Prototype's Filters
 and must be first in the List.  Second one is placeholder for Prototype's
Filters.

See source code of ``h10n.tests.filter_test`` for usage examples.
"""

class FilterChain(object):
    """ Filter Chain

    Constructor arguments:
        helpers
            Helper Namespace

    Attributes:
        helpers
            Helper Namespace
        filters
            List of compiled filters.
    """

    def __init__(self, helpers):
        self.helpers = helpers
        self.filters = []

    def apply(self, params):
        """ Apply filters to parameters

        Arguments:
            params
                Dictionary to filter.
        """
        for filter in self.filters:
            filter(params)

    def clone(self, filters):
        """ Create new Filter Chain using current one as prototype

        Arguments:
            filters
                List of Filter Definitions to compile and extend (or override)
                current Filters.

        Returns new Filter Chain based on current one.
        """
        result = self.__class__(self.helpers)
        if not filters:
            result.filters.extend(self.filters)
        else:
            if filters[0] == '__no_prototype__':
                # Without prototype filters
                result.filters.extend(self._compile(filters[1:]))
            else:
                # With prototype filters
                if '__prototype__' not in filters:
                    # Prototype filters implicit goes first
                    filters.insert(0, '__prototype__')
                p = filters.index('__prototype__')
                result.filters.extend(self._compile(filters[:p]))
                result.filters.extend(self.filters)
                result.filters.extend(self._compile(filters[p + 1:]))
        return result

    def _compile(self, filters):
        """ Compile Filters

        Arguments:
            filters
                List of filter definitions to compile without directives.

        Yields compiled filter or sting command.
        """
        for method_name, in_, out_ in filters:
            method_name = method_name.split('.')
            method = self.helpers
            for name in method_name:
                method = getattr(method, name)
            yield _compile_filter(method, in_, out_)


_template = 'def f(kw): ({out_}) = method({in_})'

def _compile_filter(method, in_, out_):
    """ Compile filter

    Returns callable, that accept single dictionary argument ``kw``.
    This callable calls ``method`` with parameters extracted from ``kw``
    according to input map ``in_``, and put result into ``kw``
    according to output map ``out_``.

    Callable is built using ``h10n.filter._template``, where ``in_`` and
    ``out_`` are input and output maps converted to string
    by ``h10n.filter._map`` function.

    See doc-strings of ``h10n.filter._map`` and ``h10n.filter._value``
    for details.

    Arguments:
        method
            Helper Method.
        in_
            Input Map.
        out_
            Output Map.  Must be string or list.  All items must be
            placeholders, i.e. strings in format "{name}".
    """
    code = _template.format(in_=_map(in_), out_=_map(out_))
    exec code in locals()
    return f

def _map(map):
    """ Map Converter

    Converts map into Python code fragment, that will be used
    in ``h10n.filter._template`` by ``h10n.filter._compile_filter``
    to construct source code of filter.

    Example::
        >>> _map({'*': [1, '{a}', '{b}.b'], 'c': '{c}["c"]'})
        '1, kw["a"], kw["b"].b, c=kw["c"]["c"]'
    """
    if hasattr(map, 'keys'):
        # When map is dict-like object
        kw = map
        args = kw.pop('*', [])
        if not hasattr(args, '__iter__'):
            args = [args]
    elif hasattr(map, '__iter__'):
        # When map is iterable object without keys (list-like)
        args = map
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
        >>> _value('Some string')
        "'Some string'"
        >>> _value('{object_from_dict}')
        'kw["object_from_dict"]'
        >>> _value('{object_from_dict}.property')
        'kw["object_from_dict"].property'
    """
    if isinstance(value, basestring) and '{' in value:
        value = value.replace('{', 'kw["').replace('}', '"]')
    else:
        value = repr(value)
    return value


if __name__ == '__main__':
    from doctest import testmod
    testmod()
