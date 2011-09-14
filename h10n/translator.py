import logging


logger = logging.getLogger(__name__)

class Translator(object):
    """ Message Translator

    Provides functional for translation messages according to current locale.

    Translator is instantiated by Locale Manager and available
    under its attribute ``translator``.
    """

    def __init__(self, locale_manager):
        self.lm = locale_manager
        self.dicts = {}

    def load(self, source):
        """ Load translations to dictionaries

        Arguments:
            source
                Translation source.  See ``h10n.source`` for details.
        """
        for locale in self.lm.locales:
            translations = self.dicts.setdefault(locale, {})
            namespace = None
            source_name = None
            for data in source[locale]:
                # Reset namespace on new source.name
                if source_name != source.name:
                    source_name = source.name
                    namespace = None
                # Setup namespace
                if 'namespace' in data:
                    namespace = data['namespace']
                # Create translation
                else:
                    try:
                        id = data['id']
                        if namespace is not None:
                            id = '{0}.{1}'.format(namespace, id)
                        translation = Translation(data, translations, self.lm.h)
                        translation.source_name = source_name
                        translations[id] = translation
                    except:
                        logger.error("Invalid translation %r "
                                     "in namespace '%s' "
                                     "from source '%s'",
                                     data, namespace, source_name,
                                     exc_info=True)

    def __call__(self, id, locale_=None, **kwargs):
        """ Translate message

        Arguments:
            id
                Translation id
            locale_
                If specified, override current locale from Locale Manager.
            **kwargs
                Keyword arguments to format translated message.
        """
        locale = locale_ or self.lm.locale
        try:
            translations = self.dicts[locale]
            try:
                return translations[id].format(**kwargs)
            except KeyError:
                logger.error("Translation '%s:%s' is not exist",
                             locale, id, exc_info=True)
            except:
                logger.error("Error in translation '%s:%s' from source '%s'",
                             locale, id, translations[id].source_name,
                             exc_info=True)
        except KeyError:
            logger.error("Translations is not loaded for locale '%s'",
                         locale, exc_info=True)
        return 'TranslationError:{0}:{1}'.format(locale, id)

    def message(self, id, **kwargs):
        """ Create lazy translatable message

        Arguments same as for ``__call__`` method.
        Returns instance of ``h10n.translator.Message``.
        """
        return Message(self, id, **kwargs)


class Message(object):
    """ Lazy translatable message

    Performs translation on convertion to ``unicode`` or ``str``.
    """

    def __init__(self, translator, id, **kwargs):
        self.translator = translator
        self.id = id
        self.kwargs = kwargs

    def __unicode__(self):
        return self.translator(self.id, **self.kwargs)

    def __str__(self):
        return unicode(self).encode(self.translator.lm.encoding)

    def __call__(self, **kwargs):
        params = self.kwargs.copy()
        params.update(kwargs)
        return self.translator(self.id, **params)

    def __repr__(self):
        return "Message('{0}')".format(self.id)


from h10n._compiler import compile_chain as _compile

class Translation(object):
    """ Translation record """

    def __init__(self, data, translations, helpers):
        # Init attributes
        self.msg = None
        self.key = None
        self.defaults = {}
        self.filters = ()
        # Update attributes from prototype
        prototype = data.get('prototype')
        if prototype is not None:
            prototype = translations[prototype]
            self.key = prototype.key
            self.msg = prototype.msg
            self.defaults.update(prototype.defaults)
            self.filters = prototype.filters
        # Update attributes from own values
        self.key = data.get('key', self.key)
        self.msg = data.get('msg', self.key)
        self.defaults.update(data.get('defaults', {}))
        # Setup filters
        filters = data.get('filters', ())
        if filters and filters[0] == '__no_prototype__':
            # Prototype filters explicit disabled
            self.filters = tuple(_compile(helpers, filters[1:]))
        elif filters and filters[-1] == '__prototype__':
            # Prototype filters explicit goes last
            self.filters = tuple(_compile(helpers, filters[:-1])) \
                         + self.filters
        else:
            # Prototype filters implicit goes first
            self.filters += tuple(_compile(helpers, filters))

    def format(self, **kw):
        params = self.defaults.copy()
        params.update(kw)
        for filter in self.filters:
            filter(params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)
