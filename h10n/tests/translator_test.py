# -*- coding: utf-8 -*-
from nose import tools

from h10n.translator import Translator


def setup():
    Translator.get_instance('test').configure(
        {
            'root': {
                'en-US': {
                    'test': {
                        'messages': {
                            'message': 'Message',
                            'fallback': 'Fallback Message',
                        }
                    }
                },
                'ru-RU': {
                    'test': {
                        'messages': {
                            'message':  u'Сообщение',
                        }
                    }
                }
            },
            'fallback': {'ru-RU': 'en-US'},
            'default': 'en-US',
        }
    )


def translator_test():
    """ Translator test """
    translator = Translator.get_instance('test')
    _ = translator.translate

    # Test default locale
    tools.eq_(_('test.message'), 'Message')

    # Test current locale
    translator.locale = 'ru-RU'
    tools.eq_(_('test.message'), u'Сообщение')

    # Test fallback
    tools.eq_(_('test.fallback'), 'Fallback Message')
    tools.eq_(_('test.invalid', fallback='Invalid Message'), 'Invalid Message')
    tools.eq_(_('test.invalid'), 'Translation Error: ru-RU.test.invalid')

    # Lazy translatable message test
    message = translator.message('test.message')
    tools.eq_(unicode(message), u'Сообщение')
