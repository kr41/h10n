# coding: utf-8

from h10n import Translator


locales = {
    'en-US': {
        'message': {
            'removed': {
                'filter': """
                    $object = self.locale['object'][$object].format()
                """,
                'msg': u'{object} has been successfully removed'
            }
        },
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

assert(t.translate('message:removed', 'Object has been removed', object='article') ==
       u'Article has been successfully removed')
assert(t.translate('message:removed', 'Object has been removed', object='comment') ==
       u'Comment has been successfully removed')

t.lang = 'ru'
assert(t.translate('message:removed', 'Object has been removed', object='article') ==
       u'Article has been successfully removed')
assert(t.translate('message:removed', 'Object has been removed', object='comment') ==
       u'Comment has been successfully removed')
