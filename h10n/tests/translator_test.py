# -*- coding: utf-8 -*-
import os
from nose import tools

from h10n.translator import Translator


def setup():
    global _
    config = {
        'locales': {
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
        'scan': 'h10n.tests:data'
    }
    translator = Translator.get_instance('test')
    translator.configure(**config)
    _ = translator.translate

def maps_test():
    """ Language and Region maps test """
    translator = Translator.get_instance('test')

    translator.language = 'ru'
    tools.eq_(_('test.message'), u'Сообщение')
    translator.region = 'US'
    tools.eq_(_('test.message'), 'Message')

def fallback_test():
    """ Translator fallback test """
    translator = Translator.get_instance('test')
    translator.locale = 'ru-RU'

    tools.eq_(_('test.fallback'), 'Fallback Message')
    tools.eq_(_('test.invalid', fallback='Invalid Message'), 'Invalid Message')
    tools.eq_(_('test.invalid'), 'Translation Error: ru-RU.test.invalid')

def fallback_test():
    """ Lazy translatable message test """
    translator = Translator.get_instance('test')
    message = translator.message('test.message')

    translator.locale = 'en-US'
    tools.eq_(unicode(message), 'Message')

    translator.locale = 'ru-RU'
    tools.eq_(unicode(message), u'Сообщение')

def fallback_test():
    """ File Sources Test """
    translator = Translator.get_instance('test')
    translator.locale = 'en-US'
    tools.eq_(_('source.message', count=4), '4 items')
    tools.eq_(_('sub-source.message'), 'Message from sub-source')
    tools.eq_(_('_skip.message'), 'Translation Error: en-US._skip.message')

def from_config_test():
    """ Translator from Config Test """
    config = {
        'h10n.instance': 'read_config_test',
        'h10n.default': 'en-US',
        'h10n.fallback.ru-RU': 'en-US',
        'h10n.locales.en-US.test.messages.message': 'Message',
        'h10n.locales.ru-RU': {},
    }
    translator = Translator.from_config(config)

    tools.eq_(translator.translate('test.message'), 'Message')
    translator.locale = 'ru-RU'
    tools.eq_(translator.translate('test.message'), 'Message')
