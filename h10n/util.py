class ExceptionContext(object):
    """ Exception Context """

    def __init__(self, obj):
        self.chain = [obj]

    def __repr__(self):
        chain = ', '.join(repr(obj) for obj in reversed(self.chain))
        return '<ExceptionContext: [{0}]>'.format(chain)

    @classmethod
    def extend(cls, exception, obj):
        """ Extends existent context of exception or add new one """
        # Search for existent context in exception arguments
        for arg in reversed(exception.args):
            if isinstance(arg, cls):
                if arg.chain[-1] is not obj:
                    arg.chain.append(obj)
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
