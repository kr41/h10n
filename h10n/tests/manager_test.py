""" The tests for Locale Manager """

from threading import Thread
from nose import tools

from h10n.manager import LocaleManager
from h10n.exception import NotConfigured


@tools.raises(NotConfigured)
def not_configured_test():
    """ Unconfigured ``LocaleManager``

    Raises ``NotConfigured`` exception on attempt to use Locale Manager
    before configuration.
    """
    lm = LocaleManager()
    lm.locale = 'en'

@tools.raises(ValueError)
def unsupported_locale_test():
    """ ``LocaleManager`` with unsupported locale

    Raises``ValueError`` exception on attempt to set unsupported locale.
    """
    lm = LocaleManager()
    lm.configure(locales=('en', 'ru'))
    lm.locale = 'cn'

def lang_test():
    """  """
    lm = LocaleManager()
    lm.configure(locales=('en-us',))
    tools.eq_(lm.lang, 'en')

def country_test():
    """  """
    lm = LocaleManager()
    lm.configure(locales=('en-us',))
    tools.eq_(lm.country, 'us')

def registry_test():
    """ Registry of ``LocaleManager`` """
    def first_call():
        return LocaleManager.get_instance('registry_test')
    def second_call():
        return LocaleManager.get_instance('registry_test')
    tools.eq_(first_call(), second_call())

def thread_local_mode_test():
    """ Thread local mode of ``LocaleManager`` """
    lm = LocaleManager()
    lm.configure(locales=('en', 'ru'), mode=lm.THREAD_LOCAL)
    # Assigns locale value in main thread
    lm.locale = 'ru'
    def thread():
        # Assign another locale value in child thread
        lm.locale = 'en'
    t = Thread(target=thread)
    t.start()
    t.join()
    # Locale value in main thread must be **unchanged**
    tools.eq_(lm.locale, 'ru')
