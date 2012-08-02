# coding: utf-8

from h10n import Translator


locales = {
    'en-US': {
        'object': {
            'article': u'Article',
            'comment': u'Comment',
        },
    },
    'ru-RU': {
        'object': {
            'article': u'Статья',
            'comment': u'Комментарий',
        },
    },
}
t = Translator(locales=locales, default='en-US')

assert(t.translate('object:article', u'Article') == u'Article')
assert(t.translate('object:comment', u'Comment') == u'Comment')

t.lang = 'ru'
assert(t.translate('object:article', u'Article') == u'Статья')
assert(t.translate('object:comment', u'Comment') == u'Комментарий')
