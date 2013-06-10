"""
An Utility module contains objects which is used by h10n internally.  End users
don't need to use this module directly.
"""


class Namespace(object):
    """
    Namespace is an utility object, which mimics to JavaScript object.
    The Namespace provides methods to manipulate attributes using subscription
    interface:

    ..  code-block:: pycon

        >>> ns = Namespace()
        >>> ns.a = 1
        >>> ns['a']
        1
        >>> ns['a'] = 2
        >>> ns.a
        2
        >>> ns['b.c'] = 3
        >>> ns.b.c
        3
        >>> ns.b                                     # doctest: +ELLIPSIS
        <h10n.util.Namespace object at ...>

    """

    _frozen = ()

    def extend(self, d):
        """
        Extends namespace by attributes from dictionary or another namespace.
        Dot-separated keys in the dictionary becomes to nested namespace.

        ..  code-block:: pycon

            >>> ns = Namespace().extend({'a.b': 1, 'c': 2})
            >>> ns.a.b
            1
            >>> ns.c
            2
            >>> ns.a                                 # doctest: +ELLIPSIS
            <h10n.util.Namespace object at ...>
            >>> ns_2 = Namespace().extend({'c': 3, 'd': 4, 'a.e': 5})
            >>> ns.extend(ns_2)                      # doctest: +ELLIPSIS
            <h10n.util.Namespace object at ...>
            >>> ns.c
            3
            >>> ns.d
            4
            >>> ns.a.e
            5

        """
        for name, value in d.items():
            if name.startswith('_') or name in self._frozen:
                continue
            self[name] = value
        return self

    def freeze(self):
        """
        Freeze current attributes of namespace to prevent overriding via
        extend.

        ..  code-block:: pycon

            >>> ns = Namespace().extend({'a': 1})
            >>> ns.freeze()
            >>> ns.extend({'a': 2}).a
            1

        """
        self._frozen = [name for name in dir(self) if not name.startswith('_')]

    def __getitem__(self, name):
        if '.' in name:
            try:
                name, tail = name.split('.', 1)
                return self.__dict__[name][tail]
            except KeyError:
                # Raise another KeyError to store proper key as argument
                raise KeyError(name)
        return self.__dict__[name]

    def __setitem__(self, name, value):
        if '.' in name:
            name, tail = name.split('.', 1)
            if name not in self.__dict__ or \
               not isinstance(self.__dict__[name], Namespace):
                self.__dict__[name] = Namespace()
            self.__dict__[name][tail] = value
        else:
            self.__dict__[name] = value

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default

    def items(self):
        for name, value in self.__dict__.items():
            if isinstance(value, Namespace):
                for subname, subvalue in value.items():
                    yield '{0}.{1}'.format(name, subname), subvalue
            else:
                yield name, value


class NamedObject(object):
    """
    An utility base class for named objects, which are useful in debugging.

    ..  code-block:: pycon

        >>> no = NamedObject()
        >>> no
        <NamedObject: __empty__>
        >>> no.name = 'test'
        >>> no
        <NamedObject: test>

    """

    name = '__empty__'

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.name)
