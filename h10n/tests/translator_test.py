# -*- coding: utf-8 -*-
from nose import tools

from h10n.translator import Translator


def setup():
    Translator.get_instance('test').configure(
        {
            'server': {
                'locales': {
                    'en-US': {
                        'catalogs': {
                            'test': {
                                'strategy': 'on_start_up',
                                'source': [
                                    {
                                        'id': 'message',
                                        'msg': 'Message',
                                    },
                                    {
                                        'id': 'fallback',
                                        'msg': 'Fallback Message',
                                    },
                                ]
                            }
                        }
                    },
                    'ru-RU': {
                        'catalogs': {
                            'test': {
                                'strategy': 'on_start_up',
                                'source': [
                                    {
                                        'id': 'message',
                                        'msg': u'Сообщение',
                                    },
                                ]
                            }
                        }
                    },
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
