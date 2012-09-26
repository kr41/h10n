# coding: utf-8

from h10n import Translator


def a(lang, country):
    if lang != 'en':
        raise ValueError('Unsupported language "{0}"'.format(lang))

    def helper_a(word):
        if word[0].lower() in ('a', 'e', 'i', 'o', 'u'):
            return 'an'
        return 'a'
    return helper_a

locales = {
    'en-US': {
        'message': {
            '__helper__': {
                'a': '__main__:a',
            },
            'removed': {
                'filter': """
                    $object = self.locale['object'][$object].format()
                """,
                'msg': u'{object} has been successfully removed'
            },
            'choose': {
                'filter': """
                    $object = self.locale['object'][$object].format().lower()
                    $an = helper.a($object)
                """,
                'msg': u'Please, choose {an} {object} for removal'
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

assert(t.translate('message:choose', 'Choose an object', object='article') ==
       u'Please, choose an article for removal')
assert(t.translate('message:choose', 'Choose an object', object='comment') ==
       u'Please, choose a comment for removal')

t.lang = 'ru'
assert(t.translate('message:choose', 'Choose an object', object='article') ==
       u'Please, choose an article for removal')
assert(t.translate('message:choose', 'Choose an object', object='comment') ==
       u'Please, choose a comment for removal')
