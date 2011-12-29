import logging

from h10n.core import Locale, HelperNamespace
from h10n.source import scanner


logger = logging.getLogger(__name__)

class Translator(object):

    _instances = {}

    @classmethod
    def get_instance(cls, name='__default__'):
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]

    @classmethod
    def from_config(cls, config, prefix='h10n.'):
        instance_key = prefix + 'instance'
        instance = config.get(instance_key, '__default__')
        config_tree = {}
        prefix_len = len(prefix)
        for key, value in config.iteritems():
            if key == instance_key:
                continue
            if key.startswith(prefix):
                key = key[prefix_len:]
                path = key.split('.')
                last = path.pop()
                branch = config_tree
                for point in path:
                    branch = branch.setdefault(point, {})
                branch[last] = value
        instance = cls.get_instance(instance)
        instance.configure(**config_tree)
        return instance

    encoding = 'utf-8'

    def __init__(self, name='__empty__'):
        self.name = name

    def configure(self, default=None, locales=None, use_only=None,
                  lang_map=None, region_map=None,
                  fallback=None, strategy='simple', scan=None, helper=None):
        self.default = default
        self.fallback = fallback or {}
        if strategy == 'simple':
            self.storage = _simple_storage()
        elif strategy == 'thread_local':
            self.storage = _thread_local_storage()
        else:
            raise ValueError('Invalid strategy "{0}"'.format(strategy))
        locales = locales or {}
        scan = _list(scan)
        use_only = _list(use_only)
        for source in scanner(scan):
            for name, catalogs in source.iteritems():
                locale = locales.setdefault(name, {})
                for catalog_name, catalog_properties in catalogs.iteritems():
                    if catalog_name in locale:
                        logger.warning('Overriding catalog %s:%s',
                                       name, catalog_name)
                    locale[catalog_name] = catalog_properties
        self.locales = {}
        self.lang_map = lang_map or {}
        self.region_map = region_map or {}
        for name, catalogs in locales.iteritems():
            if use_only and name not in use_only:
                continue
            locale = Locale(name, self, catalogs)
            self.locales[name] = locale
            if lang_map is None or locale.lang not in lang_map:
                self.lang_map[locale.lang] = name
            if region_map is None or locale.region not in region_map:
                self.region_map[locale.region] = name
        if self.default is None:
            self.default = self.locales.keys()[0]
        if helper:
            for locale in self.locales.itervalues():
                locale.helper = HelperNamespace(locale, helper)

    @property
    def locale(self):
        return self.storage.__dict__.get('locale', self.default)

    @locale.setter
    def locale(self, locale):
        if locale not in self.locales:
            raise ValueError('Unsupported locale "{0}"'.format(locale))
        self.storage.locale = locale

    @property
    def lang(self):
        return self.locales[self.locale].lang

    @lang.setter
    def lang(self, lang):
        if lang not in self.lang_map:
            raise ValueError('Unsupported lang "{0}"'.format(lang))
        self.locale = self.lang_map[lang]

    @property
    def region(self):
        return self.locales[self.locale].region

    @region.setter
    def region(self, region):
        if region not in self.region_map:
            raise ValueError('Unsupported region "{0}"'.format(region))
        self.locale = self.region_map[region]

    @property
    def helper(self):
        return self.locales[self.locale].helper

    def translate(self, id, fallback=None, locale=None, **params):
        failed_locales = []
        locale = locale or self.locale
        logger.debug('Translate %s:%s', locale, id)
        if fallback is None:
            logger.warning('Empty fallback message on translate %s', id)
        while True:
            try:
                return self.locales[locale][id].format(**params)
            except Exception:
                logger.error('Translation error %s:%s',
                             locale, id, exc_info=True)
                failed_locales.append(locale)
                fallback_locale = self.fallback.get(locale)
                if not fallback_locale or fallback_locale in failed_locales:
                    break
                locale = fallback_locale
                logger.debug('Fallback to %s', locale)
        if fallback is None:
            fallback = 'Translation Error: {0}:{1}'.format(self.locale, id)
        return fallback

    def message(self, id, fallback=None, **params):
        return Message(self, id, fallback, **params)


class Message(object):

    def __init__(self, translator, id, fallback=None, **params):
        if isinstance(translator, basestring):
            translator = Translator.get_instance(translator)
        self.translator = translator
        self.id = id
        self.fallback = fallback
        self.params = params
        if fallback is None:
            logger.warning('Empty fallback message in %r', self)

    def __call__(self, fallback=None, **params):
        if params:
            p = self.params.copy()
            p.update(params)
            params = p
        else:
            params = self.params
        fallback = fallback or self.fallback
        return self.translator.translate(self.id, fallback, **params)

    def __repr__(self):
        return '<Message: {0}>'.format(self.id)

    def __unicode__(self):
        return self.translator.translate(self.id, self.fallback, **self.params)

    def __str__(self):
        return unicode(self).encode(self.translator.encoding)

    def __mod__(self, right):
        return unicode(self) % right


from threading import local as _thread_local_storage

class _simple_storage(object):
    """ An utility class to store values """
    pass

def _list(value):
    if value is None:
        value = []
    if isinstance(value, basestring):
        value = [item.strip() for item in value.split(',')]
    return value
