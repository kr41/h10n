# -*- coding: utf-8 -*-
from nose import tools
from threading import Thread

from h10n.translator import Translator


def setup():
    translator = Translator.get_instance('translator_test')
    translator.configure(
        locales={
            'en-US': {
                'test': {
                    'message': 'Message',
                    'fallback': 'Fallback Message',
                }
            },
            'ru-RU': {
                'test': {
                    'message':  u'Сообщение',
                }
            }
        },
        fallback={'ru-RU': 'en-US', 'en-US': 'ru-RU'},
        default='en-US',
    )

def maps_test():
    translator = Translator.get_instance('translator_test')

    tools.eq_(translator.lang_map, {'en': 'en-US', 'ru': 'ru-RU'})
    tools.eq_(translator.region_map, {'US': 'en-US', 'RU': 'ru-RU'})
    translator.lang = 'ru'
    tools.eq_(translator.translate('test:message'), u'Сообщение')
    translator.region = 'US'
    tools.eq_(translator.translate('test:message'), 'Message')

def fallback_test():
    translator = Translator.get_instance('translator_test')
    translator.locale = 'ru-RU'

    tools.eq_(translator.translate('test:fallback'), 'Fallback Message')
    tools.eq_(translator.translate('test:invalid', fallback='Invalid Message'),
              'Invalid Message')
    tools.eq_(translator.translate('test:invalid'),
              'Translation Error: ru-RU:test:invalid')

def from_config_test():
    config = {
        'h10n.instance': 'read_config_test',
        'h10n.default': 'en-US',
        'h10n.fallback.ru-RU': 'en-US',
        'h10n.locales.en-US.test.message': 'Message',
        'h10n.locales.ru-RU': {},
    }
    translator = Translator.from_config(config)

    tools.eq_(translator.translate('test:message'), 'Message')
    translator.locale = 'ru-RU'
    tools.eq_(translator.translate('test:message'), 'Message')

def thread_local_strategy_test():
    config = {
        'strategy': 'thread_local',
        'default': 'en-US',
        'locales': {'en-US': {}, 'ru-RU': {}},
    }
    translator = Translator.get_instance('thread_local_test')
    translator.configure(**config)
    def worker():
        translator = Translator.get_instance('thread_local_test')
        translator.locale = 'en-US'
    translator.locale = 'ru-RU'
    thread = Thread(target=worker)
    thread.start()
    thread.join()
    tools.eq_(translator.locale, 'ru-RU')
