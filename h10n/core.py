import re
from textwrap import dedent
from threading import RLock

from h10n.util import keep_context
from h10n.util import NamedObject
from h10n import helpers as generic


class Locale(NamedObject):
    """ Locale """

    @keep_context
    def __init__(self, name, translator=None, catalogs=None):
        self.name = name
        self.translator = translator
        self.lang, self.country = name.split('-')
        self.catalogs = {'__prototype__': Message()}
        for catalog_name, catalog in catalogs.iteritems():
            if catalog_name in self.catalogs:
                raise ValueError('Duplicate catalog name "{0}": {1}'.
                                 format(catalog_name, repr(catalog)))
            self.catalogs[catalog_name] = Catalog(catalog_name, self, catalog)

    @keep_context
    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.catalogs[name][tail]
        return self.catalogs[name]


class Catalog(NamedObject):
    """ Message Catalog """

    @keep_context
    def __init__(self, name, locale, config):
        self.name = name
        self.locale = locale
        self._mutex = RLock()
        # Create messages
        factory = config.pop('factory', None)
        if factory is None and 'messages' in config:
            self.messages = config['messages']
        else:
            self.messages = factory(**config)
        # Create helpers namespace
        self.helpers = {'generic': generic, '__builtins__': __builtins__}
        imports = self.messages.get('__helpers__')
        if imports:
            exec dedent(imports) in locals(), self.helpers

    @keep_context
    def __getitem__(self, id):
        result = self.messages[id]
        if not isinstance(result, Message):
            with self._mutex:
                if isinstance(result, basestring):
                    result = {'msg': result}
                result = self.messages[id] = Message(id, self, **result)
        return result

    @keep_context
    def get_prototype(self, name):
        return self.locale[name or '__prototype__']


class Message(NamedObject):
    """ Localized Message """

    key = None
    msg = None
    filter = None
    defaults = {}

    _parser = re.compile('\$([a-z_]{1}[a-z_0-9]*)', re.I)

    @keep_context
    def __init__(self, name='__prototype__', catalog=None, prototype=None,
                 key=None, msg=None, defaults=None, filter=None):
        self.name = name
        self.catalog = catalog
        if self.catalog is None:
            return
        prototype = self.catalog.get_prototype(prototype)
        self.key = key or prototype.key
        self.msg = msg or prototype.msg
        self.defaults = prototype.defaults.copy()
        if defaults:
            self.defaults.update(defaults)
        if filter:
            filter = dedent(filter)
            helpers = self.catalog.helpers
            if '__prototype__' in filter:
                prototype_call = '__prototype__.filter(__locale__, kw)' \
                                 if prototype.filter else ''
                filter = filter.replace('__prototype__', prototype_call)
                helpers = helpers.copy()
                helpers['__prototype__'] = prototype
            filter = self._parser.sub(r'kw["\g<1>"]', filter)
            code = ['def filter(__locale__, kw):']
            code.extend(filter.split('\n'))
            code = '\n    '.join(code)
            exec code in helpers, self.__dict__

    @keep_context
    def format(self, **kw):
        """ Format Message according to passed parameters """
        params = self.defaults.copy()
        params.update(kw)
        if self.filter:
            self.filter(self.catalog.locale, params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)
