from h10n.exception import NotConfigured
from h10n.helper import HelperManager
from h10n.translator import Translator


class LocaleManager(object):
    """ Locale Manager

    Provides functional to manage locales and translations.

    An instance must be configured before any usage.
    See ``LocaleManager.configure`` for details.

    Also, provides registry functional to share single instance between several
    independent modules.  See ``LocaleManager.get_instance`` for details.

    Attributes:
        locales
            List of supported locales.
        default
            Default locale (first item from ``locales``).
        locale
            Current locale.  In thread local mode this value is local
            for each thread.  Attempt to setup value that not in ``locales``
            raises ``ValueError``.
        translator
            Translator object (callable).  See ``h10n.translator.Translator``
            for details.
        h
            Helper Manager.  See ``h10n.helper.HelperManager`` for details.
    """

    _instances = {}

    @classmethod
    def get_instance(cls, app_name='__default__'):
        """ Get instance of Locale Manager by application name

        Provides registry functional to share single Locale Manager between
        several independent modules.  For example, WSGI-middleware, that setup
        locale according to request parameters, and WSGI-application,
        that performs translations.
        """
        if app_name not in cls._instances:
            cls._instances[app_name] = cls()
        return cls._instances[app_name]

    encoding = 'utf-8'

    SIMPLE = 'simple'
    THREAD_LOCAL = 'thread_local'

    def __init__(self):
        self.h = HelperManager(self)
        self.translator = Translator(self)
        self._configured = False

    def configure(self, locales, mode=SIMPLE):
        """ Configure Locale Manager

        Arguments:
            locales
                List of supported locales.
            mode
                Case of 'simple' for non-threading mode and 'thread_local'
                for thread local mode.
        """
        if mode == self.SIMPLE:
            storage = _simple_storage()
        elif mode == self.THREAD_LOCAL:
            storage = _thread_local_storage()
        else:
            raise ValueError("Invalid mode '{0}'".format(mode))
        self._storage = storage
        self.locales = locales
        self.default = locales[0]
        self._configured = True

    def __getattr__(self, item):
        if not self._configured:
            raise NotConfigured("Locale Manager is not configured yet")
        # Mimics to standard error message
        raise AttributeError("'{class_}' object has no attribute '{item}'".
                             format(class_=self.__class__.__name__, item=item))

    @property
    def locale(self):
        """ Current locale.

        In thread local mode this value is local for each thread.
        Attempt to setup value that is not supported locale value
        raises ``ValueError``
        """
        self._check_locale()
        return self._storage.locale

    @locale.setter
    def locale(self, locale):
        if locale not in self.locales:
            raise ValueError("Unsupportable locale '{0}'".format(locale))
        self._set_locale(locale)

    @property
    def country(self):
        """ Current country.

        If locale is in format ``xx-yy`` (for example ``en-us``),
        this property conatains ``yy``.
        Otherwise, this value is equal to current locale.
        """
        self._check_locale()
        return self._storage.country

    @property
    def lang(self):
        """ Current language.

        If locale is in format ``xx-yy``, (for example ``en-us``)
        this property conatains ``xx``.
        Otherwise, this value is equal to current locale.
        """
        self._check_locale()
        return self._storage.lang

    def _set_locale(self, locale):
        """ Set locale value """
        self._storage.locale = locale
        if '-' in locale:
            self._storage.lang, self._storage.country = locale.split('-')
        else:
            self._storage.lang = self._storage.country = locale

    def _check_locale(self):
        """ Check storage

        If storage is not initialized, set default locale
        """
        if not hasattr(self._storage, 'locale'):
            self._set_locale(self.default)

from threading import local as _thread_local_storage

class _simple_storage(object):
    """ An utility class to store values """
    pass
