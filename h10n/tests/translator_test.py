# -*- coding: utf-8 -*-

""" The tests for Translator """

from nose import tools

from h10n.manager import LocaleManager
from h10n.tests import data


def setup():
    global message, _

    # Create and configure Locale Manager
    lm = LocaleManager.get_instance('test')
    lm.configure(locales=('en', 'ru'))
    lm.h.bind_helper('test', data.TestHelper())
    lm.translator.load(data.simple_source)
    lm.translator.load(data.complex_source)

    # Create aliases
    # Translation function (mimics to gettext)
    _ = lm.translator
    # Lazy Translatable Message Factory (mimics to regular class)
    Message = lm.translator.message

    # Create lazy translatable message
    message = Message('day.friday')


def simple_translation_test():
    """ Simple translations """
    lm = LocaleManager.get_instance('test')
    lm.locale = 'en'
    tools.eq_(_('day.monday'), u'Monday')
    lm.locale = 'ru'
    tools.eq_(_('day.monday'), u'Понедельник')

def message_test():
    """ Lazy translations """
    lm = LocaleManager.get_instance('test')
    lm.locale = 'en'
    tools.eq_(unicode(message), u'Friday')
    lm.locale = 'ru'
    tools.eq_(unicode(message), u'Пятница')

def message_str_encoding_test():
    """ Translation encoding """
    lm = LocaleManager.get_instance('test')
    lm.locale = 'ru'
    tools.eq_(str(message), u'Пятница'.encode('utf-8'))

def complex_translation_test():
    """ Complex translations """
    lm = LocaleManager.get_instance('test')
    lm.locale = 'en'
    tools.eq_(_('confirm.delete', count=1, object='file'),
              u'Are you sure you want to delete 1 file?')
    tools.eq_(_('confirm.delete', count=2, object='file'),
              u'Are you sure you want to delete 2 files?')
    lm.locale = 'ru'
    tools.eq_(_('confirm.delete', count=1, object='file'),
              u'Вы уверены, что хотите удалить 1 файл?')
    tools.eq_(_('confirm.delete', count=2, object='file'),
              u'Вы уверены, что хотите удалить 2 файла?')
    tools.eq_(_('confirm.delete', count=5, object='file'),
              u'Вы уверены, что хотите удалить 5 файлов?')
