import re
from textwrap import dedent
from threading import RLock

from h10n.util import keep_context
from h10n.util import NamedObject, Namespace
from h10n import helpers as generic


class Locale(NamedObject):
    """ Locale """

    @keep_context
    def __init__(self, name, translator=None, catalogs=None):
        self.name = name
        self.translator = translator
        self.lang, self.region = name.split('-')
        self.catalogs = {}
        for catalog_name, catalog in catalogs.iteritems():
            if catalog_name in self.catalogs:
                raise ValueError('Duplicate catalog name "{0}": {1}'.
                                 format(catalog_name, repr(catalog)))
            self.catalogs[catalog_name] = Catalog(catalog_name, self, catalog)

    @keep_context
    def __getitem__(self, name):
        if ':' in name:
            name, tail = name.split(':', 1)
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
        if 'factory' in config and callable(config['factory']):
            factory = config.pop('factory', None)
            self.source = factory(**config)
        else:
            self.source = config
        # Create helpers namespace
        self.helpers = {}
        imports = self.source.get('__helpers__')
        if imports:
            exec dedent(imports) in locals(), self.helpers
        # Create prototypes namespace
        self.prototypes = {}
        imports = self.source.get('__prototypes__')
        if imports:
            exec dedent(imports) in locals(), self.prototypes


    @keep_context
    def __getitem__(self, name):
        message = self.source[name]
        if not isinstance(message, Message):
            with self._mutex:
                if isinstance(message, basestring):
                    message = {'msg': message}
                prototype = message.pop('prototype', None)
                if prototype:
                    prototype = self.prototypes.get(prototype) or \
                                self.locale[prototype]
                message = self.source[name] = Message(name, self.locale,
                                                      helpers=self.helpers,
                                                      prototype=prototype,
                                                      **message)
        return message


class Message(NamedObject, Namespace):
    """ Localized Message """

    _parser = re.compile('\$([a-z_]{1}[a-z_0-9]*)', re.I)

    @keep_context
    def __init__(self, name='__empty__', locale=None, prototype=None,
                 key=None, msg=None, defaults=None, filter=None, helpers=None,
                 **properties):
        self.name = name
        self.locale = locale
        self.key = key
        self.msg = msg
        self.filter = None
        self.defaults = {}
        self.prototype = prototype
        names = self.__dict__.keys()
        if self.prototype:
            self.key = self.key or self.prototype.key
            self.msg = self.msg or self.prototype.msg
            self.defaults.update(self.prototype.defaults)
            self.extend(self.prototype, skip=names)
        self.defaults.update(defaults or {})
        self.extend(properties, skip=names)
        if filter is None and self.prototype and self.prototype.filter:
            filter = '__prototype__'
        if filter:
            namespace = {
                'generic': generic,
                'self': self,
                '__builtins__': __builtins__,
                '__prototype__': prototype,
                '__locale__': self.locale,
            }
            namespace.update(helpers or {})
            filter = dedent(filter)
            if '__prototype__' in filter:
                if self.prototype and self.prototype.filter:
                    prototype_call = 'self.prototype.filter(self, kw)'
                else:
                    prototype_call = ''
                filter = filter.replace('__prototype__', prototype_call)
            filter = self._parser.sub(r'kw["\g<1>"]', filter)
            filter = filter.split('\n')
            filter.insert(0, 'def filter(self, kw):')
            filter = '\n    '.join(filter)
            exec filter in namespace, self.__dict__

    @keep_context
    def format(self, **kw):
        """ Format Message according to passed parameters """
        params = self.defaults.copy()
        params.update(kw)
        if self.filter:
            self.filter(self, params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)
