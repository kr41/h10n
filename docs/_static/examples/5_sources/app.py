# app.py
# coding: utf-8

import os

from h10n import Translator

path = os.path.join(os.path.dirname(__file__), 'translations')
t = Translator(scan='path://' + path, default='en-US')

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
assert(t.translate('message:choose', 'Choose an object', object='article') ==
       u'Please, choose an article for removal')
assert(t.translate('message:choose', 'Choose an object', object='comment') ==
       u'Please, choose a comment for removal')

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
assert(t.translate('message:choose', 'Choose an object', object='article') ==
       u'Выберете статью для удаления')
assert(t.translate('message:choose', 'Choose an object', object='comment') ==
       u'Выберете комментарий для удаления')
