import logging

from h10n.core import Server


logger = logging.getLogger(__name__)

class Translator(object):

    _instances = {}

    @classmethod
    def get_instance(cls, name='__default__'):
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]

    encoding = 'utf-8'

    def __init__(self, name):
        self.name = name

    def configure(self, config):
        self.default = config['default']
        self.fallback = config.get('fallback', {})
        self.strategy = config.get('strategy', 'simple')
        if self.strategy == 'simple':
            self.storage = _simple_storage
        elif self.strategy == 'thread_local':
            self.storage = _thread_local_storage
        else:
            raise ValueError('Invalid strategy "{0}"'.format(self.strategy))
        self.server = Server(self.name, config['server'])
    @property
    def locale(self):
        return self.storage.__dict__.get('locale', self.default)

    @locale.setter
    def locale(self, locale):
        if locale not in self.server.locales:
            raise ValueError('Unsupported locale "{0}"'.format(locale))
        self.storage.locale = locale

    def translate(self, id, fallback=None, **params):
        failed_locales = []
        locale = self.locale
        logger.debug('Translate %s.%s', locale, id)
        if fallback is None:
            logger.warning('Empty fallback message on translate %s', id)
        while True:
            try:
                return self.server[locale][id].format(**params)
            except Exception:
                logger.error('Translation error %s.%s',
                             locale, id, exc_info=True)
                failed_locales.append(locale)
                fallback_locale = self.fallback.get(locale)
                if not fallback_locale or fallback_locale in failed_locales:
                    break
                locale = fallback_locale
                logger.debug('Fallback to %s', locale)
        if fallback is None:
            fallback = 'Translation Error: {0}.{1}'.format(self.locale, id)
        return fallback

    def message(self, id, fallback=None, **params):
        return Message(self, id, fallback, **params)


class Message(object):

    def __init__(self, translator, id, fallback, **params):
        if isinstance(translator, basestring):
            translator = Translation.get_instance(translator)
        self.translator = translator
        self.id = id
        self.fallback = fallback
        self.params = params
        if fallback is None:
            logger.warning('Empty fallback message in %r', self)

    def __repr__(self):
        return '<Message: {0}>'.format(self.id)

    def __unicode__(self):
        return self.translator.translate(self.id, self.fallback, **self.params)

    def __str__(self):
        return unicode(self).encode(self.translator.encoding)


from threading import local as _thread_local_storage

class _simple_storage(object):
    """ An utility class to store values """
    pass
