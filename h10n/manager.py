from threading import local

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
            self._simple_mode()
        elif mode == self.THREAD_LOCAL:
            self._thread_local_mode()
        else:
            raise ValueError("Invalid mode '{0}'".format(mode))
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
        return self._get_locale()

    @locale.setter
    def locale(self, locale):
        if locale not in self.locales:
            raise ValueError("Unsupportable locale '{0}'".format(locale))
        self._set_locale(locale)

    def _simple_mode(self):
        """ Setup Locale Manager simple (non-threading) usage """
        self._locale = None
        def getter():
            return self._locale or self.default
        def setter(locale):
            self._locale = locale
        setattr(self, '_get_locale', getter)
        setattr(self, '_set_locale', setter)

    def _thread_local_mode(self):
        """ Setup Locale Manager thread local usage """
        self._locals = local()
        def getter():
            return self._locals.__dict__.get('_locale') or self.default
        def setter(locale):
            self._locals._locale = locale
        setattr(self, '_get_locale', getter)
        setattr(self, '_set_locale', setter)
