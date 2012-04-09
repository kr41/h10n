Helpers
=======

It's time to resolve the problem with indefinite article forms from previous 
topic.  The code is very simple:

..  code-block:: python

    def a(word):
        if word[0].lower() in ('a', 'o', 'i', 'e'):
            return 'an'
        return 'a'

So, you can include it directly in your filter, but it will be better to make 
this code reusable.

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

    print t.translate('message:choose', 'Choose an object', object='article')
    print t.translate('message:choose', 'Choose an object', object='comment')

    t.lang = 'ru'
    print t.translate('message:choose', 'Choose an object', object='article')
    print t.translate('message:choose', 'Choose an object', object='comment')

Take a notice to ``__helper__`` key in ``message`` catalog.  It is not a message
definition, it's a helper namespace one.  Helper namespace is provided as global 
value during filter compilation.  So, you can get access to it from filter using 
``helper`` identifier.

Keys of helper namespace definition dictionary become aliases of helpers.  
Values must be Python names of helper factories.  The format of entry point from
``pkg_resources`` is used for these names, i.e. name is defined as 
``package.name:factory``.

Helper factory must be a callable, which accept two positional arguments: 
language and country.  The returned value of factory is used by helper namespace
as helper.  There are no requirements of how to use passed arguments or which
value to return.

Here we created one helper ``a`` in helper namespace, which is constructed by
factory ``helper_a`` from current file.  Take a notice, helper usage is limited
by English language only.
