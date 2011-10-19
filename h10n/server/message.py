""" Message Module

Provides function to build Localized Messages.
"""

from h10n.server.filter import FilterChain


class Message(object):
    """ Localized Message """

    def __init__(self, locale=None):
        self.locale = locale
        self.key = None
        self.msg = None
        self.defaults = {}
        self.filters = FilterChain(locale.helpers) if locale else None

    def clone(self, key=None, msg=None, defaults=None, filters=None):
        """ Create new Message using current as Prototype """
        result = self.__class__()
        result.key = key or self.key
        result.msg = msg or self.msg
        result.defaults.update(self.defaults)
        result.defaults.update(defaults or {})
        result.filters = self.filters.clone(filters or [])
        return result

    def format(self, **kw):
        """ Format Message according to passed parameters """
        params = self.defaults.copy()
        params.update(kw)
        self.filters.apply(params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)
