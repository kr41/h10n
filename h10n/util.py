class Namespace(object):

    _frozen = ()

    def extend(self, d):
        for name, value in d.iteritems():
            if name.startswith('_') or name in self._frozen:
                continue
            self[name] = value
        return self

    def freeze(self):
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

    def iteritems(self):
        for name, value in self.__dict__.iteritems():
            if isinstance(value, Namespace):
                for subname, subvalue in value.iteritems():
                    yield '{0}.{1}'.format(name, subname), subvalue
            else:
                yield name, value


class NamedObject(object):

    name = '__empty__'

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.name)


class ExceptionContext(NamedObject):
    """ Exception Context """

    def __init__(self, obj):
        self.chain = [obj]

    @property
    def name(self):
        return repr(self.chain)

    @classmethod
    def extend(cls, exception, obj):
        """ Extends existent context of exception or add new one """
        # Search for existent context in exception arguments
        for arg in reversed(exception.args):
            if isinstance(arg, cls):
                if obj not in arg.chain:
                    arg.chain.insert(0, obj)
                raise
        # Create new context and add it to the end of exception's arguments
        exception.args += (cls(obj),)
        raise


def keep_context(method):
    """ Includes context into exception raised from decorated method """
    def context_keeper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception, e:
            ExceptionContext.extend(e, self)
    context_keeper.__name__ = method.__name__
    context_keeper.__doc__ = method.__doc__
    return context_keeper
