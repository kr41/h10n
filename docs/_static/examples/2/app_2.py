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
        'message': {
            'removed': {
                'filter': """
                    $object = self.locale['object'][$object]
                    $gender = $object.gender
                    $object = $object.format()
                """,
                'key': '{gender}',
                'msg': {
                    'm': u'{object} успешно удален',
                    'f': u'{object} успешно удалена',
                    'n': u'{object} успешно удалено',
                }
            }
        },
        'object': {
            'article': {
                'msg': u'Статья',
                'gender': 'f',
            },
            'comment': {
                'msg': u'Комментарий',
                'gender': 'm',
            },
        },
    },
}
t = Translator(locales=locales, default='en-US')

assert(
    t.translate('message:removed',
                'Object has been removed',
                object='article') == u'Article has been successfully removed'
)
assert(
    t.translate('message:removed',
                'Object has been removed',
                object='comment') == u'Comment has been successfully removed'
)

t.lang = 'ru'
assert(
    t.translate('message:removed',
                'Object has been removed',
                object='article') == u'Статья успешно удалена'
)
assert(
    t.translate('message:removed',
                'Object has been removed',
                object='comment') == u'Комментарий успешно удален'
)
