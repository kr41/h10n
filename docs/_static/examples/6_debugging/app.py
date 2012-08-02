from logging import basicConfig, DEBUG
from h10n import Translator


basicConfig(level=DEBUG)

locales = {
    'en-US': {
        'test': {
            'error': {
                'msg': '...',
                'filter': 'raise Exception("Raised from filter")',
            }
        }
    },
    'en-GB': {
        'test': {},
    },
    'ru-RU': {},
}
t = Translator(locales=locales, default='en-US', fallback={'ru-RU': 'en-GB'})

t.locale = 'ru-RU'
assert(t.translate('test:error', 'Error') == 'Error')
