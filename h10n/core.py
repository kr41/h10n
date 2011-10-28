import re
from textwrap import dedent

from h10n.util import keep_context
from h10n.util import NamedObject
from h10n import helpers as generic


class Root(NamedObject):
    """ Localization Root """

    @keep_context
    def __init__(self, name, locales):
        self.name = name
        self.locales = {}
        for name, locale in locales.iteritems():
            self.locales[name] = Locale(name, self, locale)

    @keep_context
    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.locales[name][tail]
        return self.locales[name]


class Locale(NamedObject):
    """ Locale """

    @keep_context
    def __init__(self, name, root, catalogs):
        self.name = name
        self.root = root
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
        factory = config.pop('factory', None)
        if factory is None and 'messages' in config:
            self.messages = config['messages']
        else:
            self.messages = factory(**config)
        self.helpers = self._import_helpers()

    @keep_context
    def __getitem__(self, id):
        result = self.messages[id]
        if not isinstance(result, Message):
            if isinstance(result, basestring):
                result = {'msg': result}
            result = self.messages[id] = Message(id, self, **result)
        return result

    @keep_context
    def _import_helpers(self):
        imports = self.messages.get('__helpers__')
        result = {'generic': generic, '__locale__': self.locale}
        if imports is not None:
            local_keys = key = local_dict = None
            local_keys = locals().keys()
            exec dedent(imports)
            local_dict = locals()
            for key, obj in local_dict.iteritems():
                if key not in local_keys:
                    result[key] = obj
        return result


class Message(NamedObject):
    """ Localized Message """

    key = None
    msg = None
    defaults = None
    filter = None

    parser = re.compile('\$([a-z_]{1}[a-z_0-9]*)', re.I)

    @keep_context
    def __init__(self, name='__prototype__', catalog=None, prototype=None,
                 key=None, msg=None, defaults=None, filter=None):
        self.name = name
        self.catalog = catalog
        if self.catalog is None:
            return
        prototype = self.catalog.locale[prototype or '__prototype__']
        self.key = key or prototype.key
        self.msg = msg or prototype.msg
        self.defaults = {}
        self.defaults.update(prototype.defaults or {})
        self.defaults.update(defaults or {})
        if filter is not None:
            helpers = self.catalog.helpers
            if '__prototype__' in filter:
                code = '__prototype__.filter(kw)' if prototype.filter else ''
                filter = filter.replace('__prototype__', code)
                helpers = helpers.copy()
                helpers['__prototype__'] = prototype
            filter = self.parser.sub(r'kw["\g<1>"]', filter)
            filter = dedent(filter)
            code = ['def f(kw):']
            code.extend(filter.split('\n'))
            code = '\n    '.join(code)
            exec code in helpers, locals()
            self.filter = f

    @keep_context
    def format(self, **kw):
        """ Format Message according to passed parameters """
        params = self.defaults.copy()
        params.update(kw)
        if self.filter:
            self.filter(params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)
