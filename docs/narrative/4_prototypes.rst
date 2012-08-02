Prototypes
==========

Let's add ``message:choose`` to Russian locale.

..  code-block:: python

    # coding: utf-8

    from h10n import Translator


    def helper_a(lang, country):
        if lang != 'en':
            raise ValueError('Unsupported language "{0}"'.format(lang))

        def a(word):
            if word[0].lower() in ('a', 'o', 'i', 'e'):
                return 'an'
            return 'a'
        return a

    locales = {
        'en-US': {
            'message': {
                '__helper__': {
                    'a': '__main__:helper_a',
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
                },
                'choose': {
                    'filter': """
                        $object = self.locale['object'][$object] \
                                      .format(case='a').lower()
                    """,
                    'msg': u'Выберете {object} для удаления'
                }
            },
            'object': {
                'article': {
                    'defaults': {'case': 'n'},
                    'key': '{case}',
                    'msg': {
                        'n': u'Статья',
                        'a': u'Статью',
                    },
                    'gender': 'f',
                },
                'comment': {
                    'defaults': {'case': 'n'},
                    'key': '{case}',
                    'msg': {
                        'n': u'Комментарий',
                        'a': u'Комментарий',
                    },
                    'gender': 'm',
                },
            },
        },
    }
    t = Translator(locales=locales, default='en-US')

    print t.translate('message:choose', 'Choose an object', object='article')
    print t.translate('message:choose', 'Choose an object', object='comment')

    t.lang = 'ru'
    print t.translate('message:choose', 'Choose an object', object='article')
    print t.translate('message:choose', 'Choose an object', object='comment')


Take a notice, nouns in Russian version of the message ``message:choose`` is
used in accusative case instead of nominative one.  So, we added appropriate
forms to ``object:article`` and ``object:comment``.  Also, we added default
value ``n`` (nominative) for ``case`` parameter.  Obviously, there is a
copy-paste work to add ``defaults`` and ``key`` parameters to each noun
in Russian locale.  Let's use prototype instead.


..  code-block:: python

    # coding: utf-8

    from h10n import Translator


    def helper_a(lang, country):
        if lang != 'en':
            raise ValueError('Unsupported language "{0}"'.format(lang))

        def a(word):
            if word[0].lower() in ('a', 'o', 'i', 'e'):
                return 'an'
            return 'a'
        return a

    locales = {
        'en-US': {
            'message': {
                '__helper__': {
                    'a': '__main__:helper_a',
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
                },
                'choose': {
                    'filter': """
                        $object = self.locale['object'][$object] \
                                      .format(case='a').lower()
                    """,
                    'msg': u'Выберете {object} для удаления'
                }
            },
            'proto': {
                'noun': {
                    'defaults': {'case': 'n'},
                    'key': '{case}',
                }
            },
            'object': {
                'article': {
                    'prototype': 'proto:noun',
                    'msg': {
                        'n': u'Статья',
                        'a': u'Статью',
                    },
                    'gender': 'f',
                },
                'comment': {
                    'prototype': 'proto:noun',
                    'msg': {
                        'n': u'Комментарий',
                        'a': u'Комментарий',
                    },
                    'gender': 'm',
                },
            },
        },
    }
    t = Translator(locales=locales, default='en-US')

    print t.translate('message:choose', 'Choose an object', object='article')
    print t.translate('message:choose', 'Choose an object', object='comment')

    t.lang = 'ru'
    print t.translate('message:choose', 'Choose an object', object='article')
    print t.translate('message:choose', 'Choose an object', object='comment')

