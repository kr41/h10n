# -*- coding: utf-8 -*-

""" The module contains test data """

from h10n.source import DictSource


simple_source = DictSource({
    'en': [
        {'namespace': 'day'},
        {'id': 'sunday', 'msg': u'Sunday'},
        {'id': 'monday', 'msg': u'Monday'},
        {'id': 'tuesday', 'msg': u'Tuesday'},
        {'id': 'wednesday', 'msg': u'Wednesday'},
        {'id': 'thursday', 'msg': u'Thursday'},
        {'id': 'friday', 'msg': u'Friday'},
        {'id': 'saturday', 'msg': u'Saturday'},
    ],
    'ru': [
        {'namespace': 'day'},
        {'id': 'sunday', 'msg': u'Воскресенье'},
        {'id': 'monday', 'msg': u'Понедельник'},
        {'id': 'tuesday', 'msg': u'Вторник'},
        {'id': 'wednesday', 'msg': u'Среда'},
        {'id': 'thursday', 'msg': u'Четверг'},
        {'id': 'friday', 'msg': u'Пятница'},
        {'id': 'saturday', 'msg': u'Суббота'},
    ],
})


complex_source = DictSource({
    'en': [
        {
            'id': 'noun',
            'defaults': {'count': 1},
            'filters': [['test.pluralize', '{count}', '{plural_form}']],
            'key': '{plural_form}',
        },
        {
            'id': 'file',
            'prototype': 'noun',
            'msg': {
                '0': 'file',
                '1': 'files',
            },
        },
        {
            'id': 'confirm.delete',
            'defaults': {'count': 1},
            'filters': [
                [
                    'test.term',
                    {'id': '{object}', 'count': '{count}'},
                    '{object}'
                ],
            ],
            'msg': u'Are you sure you want to delete {count} {object}?',
        },
    ],
    'ru': [
        {
            'id': 'noun',
            'defaults': {'count': 1, '{case}': 'I'},
            'filters': [['test.pluralize', '{count}', '{plural_form}']],
            'key': '{plural_form}:{case}',
        },
        {
            'id': 'file',
            'prototype': 'noun',
            'msg': {
                '0:I': u'файл',
                '0:R': u'файла',
                '0:D': u'файлу',
                '0:V': u'файл',
                '0:T': u'файлом',
                '0:P': u'файле',

                '1:I': u'файла',
                '1:R': u'файлов',
                '1:D': u'файлам',
                '1:V': u'файла',
                '1:T': u'файлами',
                '1:P': u'файлах',

                '2:I': u'файлов',
                '2:R': u'файлов',
                '2:D': u'файлам',
                '2:V': u'файлов',
                '2:T': u'файлами',
                '2:P': u'файлах',
            },
        },
        {
            'id': 'confirm.delete',
            'defaults': {'count': 1},
            'filters': [
                [
                    'test.term',
                    {'id': '{object}', 'count': '{count}', 'case': 'V'},
                    '{object}'
                ],
            ],
            'msg': u'Вы уверены, что хотите удалить {count} {object}?',
        },
    ],
})


class TestHelper(object):
    """ Test Helper """

    def bind(self, locale_manager):
        self.lm = locale_manager

    def term(self, id, **kw):
        """ Return term specified by ``id`` formatted according to ``kw`` """
        return self.lm.translator(id, **kw)

    def pluralize(self, count):
        """ Return plural form for specified ``count`` in current locale """
        lang = self.lm.locale
        if lang == 'en':
            return 0 if count == 1 else 1
        if lang == 'ru':
            mod10 = count % 10
            mod100 = count % 100
            if mod10 == 1 and mod100 != 11:
                return 0
            elif mod10 >= 2 and mod10 <= 4 and (mod100 < 10 or mod100 >= 20):
                return 1
            else:
                return 2
