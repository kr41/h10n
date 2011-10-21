class h10nException(Exception):
    """ Base h10n Exception """

class NotConfigured(h10nException):
    """ Raised on attempt to use unconfigured Locale Manager """


class Context(object):
    """ Exception Context """

    def __init__(self, obj):
        self.chain = [obj]

    def __repr__(self):
        chain = ', '.join(repr(obj) for obj in reversed(self.chain))
        return '<Context: [{0}]>'.format(chain)

    @classmethod
    def extend(cls, exception, obj):
        """ Extends existent context of exception or add new one """
        # Search for existent context in exception arguments
        for arg in reversed(exception.args):
            if isinstance(arg, cls):
                arg.chain.append(obj)
                return
        # Create new context and add it to the end of exception's arguments
        exception.args += (cls(obj),)

def keep_context(**kw):
    """ Includes context into exception raised from decorated function """
    def decorator(method):
        def context_keeper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception, e:
                obj = kw.get('context', None)
                if obj is None and args:
                    obj = args[0]
                Context.extend(e, obj)
                raise
        context_keeper.__name__ = method.__name__
        context_keeper.__doc__ = method.__doc__
        return context_keeper
    return decorator
