from h10n.server.message import Message
from h10n.exception import keep_context
from h10n.exception import NamedContext
from h10n.exception import Context


class Server(object):
    """ Localization Server """

    def __init__(self, locales):
        self.locales = {}
        for name, locale in locales.iteritems():
            self.locales[name] = Locale(name=name, **locale)

    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.locales[name][tail]
        return self.locales[name]


class Locale(object):
    """ Locale """

    def __init__(self, name, catalogs):
        self.name = name
        try:
            self.lang, self.country = name.split('-')
            self.catalogs = {'__prototype__': Message(locale=self)}
            for catalog_name, catalog in catalogs.iteritems():
                try:
                    if catalog_name in self.catalogs:
                        raise ValueError(
                            'Duplicate catalog name "{0}": {1}'.format(
                                catalog_name, repr(catalog)
                            )
                        )
                    self.catalogs[catalog_name] = Catalog(name=catalog_name,
                                                          locale=self,
                                                          **catalog)
                except Exception, e:
                    Context.extend(e, NamedContext('Catalog', catalog_name))
        except Exception, e:
            Context.extend(e, NamedContext('Locale', name))

    def __repr__(self):
        return '<Locale: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.catalogs[name][tail]
        return self.catalogs[name]

    def get_helper(self, name):
        pass


class Catalog(object):
    """ Message Catalog """

    def __init__(self, name, locale, source, strategy=None):
        self.name = name
        try:
            self.locale = locale
            # Detect strategy if no provided one
            if strategy is None:
                if hasattr(source, 'strategy'):
                    strategy = source.strategy
            # Compile messages on demand...
            if strategy == 'on_demand':
                self.source = source
            # ...or on start-up and store compiled ones in memory
            elif strategy == 'on_start_up':
                self.source = {}
                for message in source:
                    id = message['id']
                    try:
                        if id in self.source:
                            raise ValueError(
                                'Duplicate message id "{0}": {1}'.format(
                                    id, message
                                )
                            )
                        self.source[id] = self._compile_message(**message)
                    except Exception, e:
                        Context.extend(
                            e,
                            NamedContext(e, NamedContext('Message', id))
                        )
            else:
                raise ValueError('Invalid strategy "{0}"'.format(strategy))
        except Exception, e:
            Context.extend(e, NamedContext('Catalog', name))

    def __repr__(self):
        return '<Catalog: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, id):
        result = self.source[id]
        # If result is not compiled message, i.e. strategy == 'on_demand'
        if not isinstance(result, Message):
            result['id'] = id
            result = self._compile_message(**result)
        return result

    @keep_context()
    def _compile_message(self, prototype='__prototype__', **message):
        prototype = self.locale[prototype]
        return prototype.clone(**message)
