from h10n import Translator


locales = {
    'en-US': {
        'object': {
            'article': u'Article',
            'comment': u'Comment',
        },
    },
}
t = Translator(locales=locales)

assert(t.translate('object:article', u'Article') == u'Article')
assert(t.translate('object:comment', u'Comment') == u'Comment')
