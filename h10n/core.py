from textwrap import dedent

from h10n.util import keep_context
from h10n.util import NamedContext
from h10n.util import Context

from h10n.helpers import GenericHelpers


class Server(object):
    """ Localization Server """

    name = '__empty__'

    @keep_context()
    def __init__(self, name, config):
        self.name = name
        self.helpers = {'generic': GenericHelpers()}
        self.helpers.update(config.get('helpers', {}))
        self.locales = {}
        for name, locale in config['locales'].iteritems():
            self.locales[name] = Locale(name, self, locale)

    def __repr__(self):
        return '<Server: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.locales[name][tail]
        return self.locales[name]


class Locale(object):
    """ Locale """

    name = '__empty__'

    @keep_context()
    def __init__(self, name, server, config):
        self.name = name
        self.server = server
        self.helpers = config.get('helpers', {})
        self.lang, self.country = name.split('-')
        self.catalogs = {'__prototype__': Message(locale=self)}
        for catalog_name, catalog in config['catalogs'].iteritems():
            if catalog_name in self.catalogs:
                raise ValueError('Duplicate catalog name "{0}": {1}'.
                                 format(catalog_name, repr(catalog)))
            self.catalogs[catalog_name] = Catalog(catalog_name, self, catalog)

    def __repr__(self):
        return '<Locale: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.catalogs[name][tail]
        return self.catalogs[name]

    @keep_context()
    def get_helper(self, name):
        if '.' in name:
            path = name.split('.')
            name = path[0]
            helper = self.helpers.get(name) or self.server.helpers[name]
            for name in path[1:]:
                helper = getattr(helper, name)
            return helper
        return self.helpers.get(name) or self.server.helpers[name]


class Catalog(object):
    """ Message Catalog """

    name = '__empty__'

    # TODO: Replace it by thread-safe true cache with invalidation on overflow
    _cache = {}

    @keep_context()
    def __init__(self, name, locale, config):
        self.name = name
        self.locale = locale
        factory = config.pop('factory', None)
        if factory is None and 'messages' in config:
            self.messages = config['messages']
        else:
            self.messages = factory(**config)

    def __repr__(self):
        return '<Catalog: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, id):
        result = self.messages[id]
        if not isinstance(result, Message):
            if isinstance(result, basestring):
                result = {'msg': result}
            result = self.messages[id] = self._compile_message(id=id, **result)
        return result

    @keep_context()
    def _compile_message(self, prototype='__prototype__', **message):
        prototype = self.locale[prototype]
        return prototype.clone(**message)


class Message(object):
    """ Localized Message """

    def __init__(self, locale, id='__prototype__'):
        self.id = id
        self.locale = locale
        self.key = None
        self.msg = None
        self.defaults = {}
        self.filters = []

    def __repr__(self):
        return '<Message: {0}>'.format(self.id)

    @keep_context()
    def clone(self, id, key=None, msg=None, defaults=None, filters=None):
        result = self.__class__(self.locale, id)
        try:
            result.key = key or self.key
            result.msg = msg or self.msg
            result.defaults.update(self.defaults)
            result.defaults.update(defaults or {})
            result.filters = self._compile_filters(filters or [])
            return result
        except Exception, e:
            Context.extend(e, result)

    @keep_context()
    def format(self, **kw):
        """ Format Message according to passed parameters """
        params = self.defaults.copy()
        params.update(kw)
        for filter in self.filters:
            filter(params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)

    _filter_template = dedent("""
        @keep_context(context=NamedContext('Filter', helper_name))
        def f(kw):
            {output} = helper(self.locale, {input})
    """)

    def _compile_filters(self, filters):
        """ Setup Filters """
        result = []
        # Copy prototype's filters at the begin of filter chain
        # if no directive provided
        if not ('__no_prototype__' in filters or '__prototype__' in filters):
            result.extend(self.filters)
        for definition in filters:
            # Process directives
            if isinstance(definition, basestring):
                if definition == '__prototype__':
                    result.extend(self.filters)
                continue
            # Compile filter
            helper_name, input, output = definition
            try:
                helper = self.locale.get_helper(helper_name)
                input = self._map(input)
                output = self._map(output)
                code = self._filter_template.format(input=input, output=output)
                exec code in locals(), globals()
                result.append(f)
            except Exception, e:
                Context.extend(e, NamedContext('Filter', helper_name))
        return result

    def _map(self, map):
        """ Map Converter

        Converts map into Python code fragment, that will be used to construct
        filter source code.
        """
        if hasattr(map, 'keys'):
            # When map is dict-like object
            kw = map
            args = kw.pop('*', [])
            if not hasattr(args, '__iter__'):
                args = [args]
        elif hasattr(map, '__iter__'):
            # When map is list-like object
            args = map
            kw = {}
        else:
            # When map is not iterable
            args = [map]
            kw = {}
        result = [self._value(arg) for arg in args]
        result.extend('{0}={1}'.format(name, self._value(arg))
                      for name, arg in kw.iteritems())
        result = ', '.join(result)
        return result

    def _value(self, value):
        """ Value converter

        Converts value into Python code fragment, that will be used to construct
        map source code.
        """
        if isinstance(value, basestring) and '{' in value:
            value = value.replace('{', 'kw["').replace('}', '"]')
        else:
            value = repr(value)
        return value
