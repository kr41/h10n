# -*- coding: utf-8 -*-
from nose import tools
from threading import Thread

from h10n.translator import Translator


def default_locale_test():
    locales = {'en-US': {}, 'ru-RU': {}}

    # Explicit setup of default locale
    translator = Translator()
    translator.configure(default='ru-RU', locales=locales)
    tools.eq_(translator.locale, 'ru-RU')

    # Implicit setup of default locale.  It must be random from available
    translator = Translator()
    translator.configure(locales=locales)
    tools.ok_(translator.locale in locales)

def maps_test():
    # Implicit map create
    translator = Translator()
    translator.configure(locales={'en-US': {}, 'ru-RU': {}})
    tools.eq_(translator.lang_map, {'en': 'en-US', 'ru': 'ru-RU'})
    tools.eq_(translator.region_map, {'US': 'en-US', 'RU': 'ru-RU'})

    # Lang property usage
    translator.lang = 'ru'
    tools.eq_(translator.lang, 'ru')
    tools.eq_(translator.region, 'RU')
    tools.eq_(translator.locale, 'ru-RU')

    # Region property usage
    translator.region = 'US'
    tools.eq_(translator.lang, 'en')
    tools.eq_(translator.region, 'US')
    tools.eq_(translator.locale, 'en-US')

    # Merge implicitly created map items with explicitly ones
    translator = Translator()
    translator.configure(locales={'en-US': {}, 'en-GB': {},
                                  'ru-KZ': {}, 'kz-KZ': {}},
                         lang_map={'en': 'en-US'},
                         region_map={'KZ': 'ru-KZ'})
    tools.eq_(translator.lang_map,
              {'en': 'en-US', 'ru': 'ru-KZ', 'kz': 'kz-KZ'})
    tools.eq_(translator.region_map,
              {'US': 'en-US', 'GB': 'en-GB', 'KZ': 'ru-KZ'})

def use_only_test():
    # As string
    translator = Translator()
    translator.configure(locales={'en-US': {}, 'ru-RU': {}},
                         use_only='ru-RU')
    tools.eq_(translator.locales.keys(), ['ru-RU'])

    # As comma-separated string
    translator = Translator()
    translator.configure(locales={'en-US': {}, 'ru-RU': {}},
                         use_only='ru-RU, en-US')
    tools.eq_(translator.locales.keys(), ['ru-RU', 'en-US'])

    # As list
    translator = Translator()
    translator.configure(locales={'en-US': {}, 'ru-RU': {}},
                         use_only=['ru-RU', 'en-US'])
    tools.eq_(translator.locales.keys(), ['ru-RU', 'en-US'])

def translate_test():
    translator = Translator()
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
    )
    translator.locale = 'ru-RU'

    tools.eq_(translator.translate('test:message'), u'Сообщение')
    tools.eq_(translator.translate('test:fallback'), 'Fallback Message')
    tools.eq_(translator.translate('test:invalid', fallback='Invalid Message'),
              'Invalid Message')
    tools.eq_(translator.translate('test:invalid'),
              'Translation Error: ru-RU:test:invalid')

locales = {'en-US': {}, 'ru-RU': {}}
def scan_test():
    # As string
    translator = Translator()
    translator.configure(
        scan='py://h10n.tests.translator_test.translator_test'
    )
    tools.eq_(translator.locales.keys(), locales.keys())

    # As comma-separated
    translator = Translator()
    translator.configure(
        scan='py://h10n.tests.translator_test.translator_test, '
             'py://h10n.tests.translator_test.translator_test:locales'
    )
    tools.eq_(translator.locales.keys(), locales.keys())

    # As list
    translator = Translator()
    translator.configure(
        scan=['py://h10n.tests.translator_test.translator_test']
    )
    tools.eq_(translator.locales.keys(), locales.keys())


def from_config_test():
    config = {
        'h10n.instance': 'read_config_test',
        # TODO: Dotted catalog name is not available in this syntax
        'h10n.locales.en-US.test.message': 'Message',
    }
    translator = Translator.from_config(config)
    tools.eq_(translator.translate('test:message'), 'Message')

def thread_local_strategy_test():
    translator = Translator.get_instance('thread_local_test')
    translator.configure(strategy='thread_local',
                         locales={'en-US': {}, 'ru-RU': {}})
    def worker():
        translator = Translator.get_instance('thread_local_test')
        translator.locale = 'en-US'
    translator.locale = 'ru-RU'
    thread = Thread(target=worker)
    thread.start()
    thread.join()
    tools.eq_(translator.locale, 'ru-RU')

def helper_test():
    translator = Translator()
    translator.configure(locales={'en-US': {}, 'ru-RU': {}},
                         helper={'pluralize': 'h10n#pluralize'})
    translator.locale = 'en-US'
    tools.eq_(translator.helper.pluralize(1), 0)
    tools.eq_(translator.helper.pluralize(3), 1)
    tools.eq_(translator.helper.pluralize(5), 1)
    translator.locale = 'ru-RU'
    tools.eq_(translator.helper.pluralize(1), 0)
    tools.eq_(translator.helper.pluralize(3), 1)
    tools.eq_(translator.helper.pluralize(5), 2)
