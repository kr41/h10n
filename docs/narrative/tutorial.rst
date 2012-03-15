Tutorial
========

Basic translation
-----------------

Let's try to create a translation for our imaginable CMS from previous topic.  
First of all we need to create translatable object types.

..  code-block:: python

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

    print t.translate('object:article', u'Article')
    print t.translate('object:comment', u'Comment')

At the moment, our application is something like traditional "Hello world" one. 
If you run this program, output will be::
    
    Article
    Comment

Firstly we defined available locales as tree of nested dictionaries.  First 
level dictionary keys becomes locale names, second level ones -- catalog names, 
third level ones -- message names.  Yes, h10n is able to store translation 
catalogs in files, and not only in files.  But for our example will be more 
useful to define all directly in source code.

Than we created a translator.

And finally, we translated messages ``article`` and ``comment`` from 
catalog ``object``.  First argument of ``translate`` method is message full 
name, i.e. catalog name and message name separated by colon. Second one is 
fallback message, which should be used by translator on fail.  

Just because we use single locale it implicitly became default and we don't 
need to provide it explicitly before translation.  But if we add another locale,
we should do it.  So, let's add Russian locale.

..  code-block:: python
    
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

    print t.translate('object:article', u'Article')
    print t.translate('object:comment', u'Comment')

    t.lang = 'ru'
    print t.translate('object:article', u'Article')
    print t.translate('object:comment', u'Comment')

Here, we added Russian locale, which is copy of English one.  Also, we defined
default locale explicitly as ``en-US``.  So, when we translate first pair of
messages, it will be translated into English.  Second pair will be translated 
into Russian, because we explicitly defined it, using ``lang`` property.  
There are ``country`` and ``locale`` ones also available, ``locale`` accepts full 
locale name, such as ``en-US``, ``lang`` and ``country`` are shortcuts for first 
and second parts of this name.  Output, as expected, will be::

    Article
    Comment
    Статья
    Комментарий


Using filters
-------------

Let's go ahead and add to our application message template.

..  code-block:: python
    
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
    t = Translator(locales=locales)

    t.lang = 'en'
    print t.translate('message:removed', 'Object has been removed', object='article')
    print t.translate('message:removed', 'Object has been removed', object='comment')

    t.lang = 'ru'
    print t.translate('message:removed', 'Object has been removed', object='article')
    print t.translate('message:removed', 'Object has been removed', object='comment') 

If you run this program, output will be::

    Article has been successfully removed
    Comment has been successfully removed
    No handlers could be found for logger "h10n.translator"
    Object has been removed
    Object has been removed

There are two interesting things.  Let's start from last one.  We don't added
catalog ``message`` into Russian locale.  So, translator used fallback message
"Object has been removed" during translation.  It also logged debug information,
but it failed with message "No handlers could be found for logger 
"h10n.translator", because we didn't configure logger.  We will do it later,
on learning h10n debug process.

Most interesting thing is ``message:removed`` translation message, which is 
defined using full form of definition.  The best way to show difference between 
full and simple forms is to look on how message object is constructed.  If you 
look into sources, you will see, that it's little bit more complex than this:

..  code-block:: python
    
    if isinstance(message, basestring):
        message = {'msg': message}
    message = Message(**message)

A translation string provided via ``msg`` keyword argument.  Other keyword 
argument is ``filter`` one.  Filter is just Python code with little ....... of 
syntax sugar.  Filter makes all dirty work on translation.  How it work?
Method ``translate`` of translator object accepts keyword arguments.  When it
find specified message, it call message's method ``format`` passing these 
arguments.  Method ``format`` process provided arguments using filter and
calls ``format`` method of translation string ``msg``, using filtered arguments.

So, string::
    
    $object = self.locale['object'][$object].format()

Becomes a function, which accept message object as first argument and dict of
keyword arguments as second one:

..  code-block:: python

    def filter(self, kw):
        kw['object'] = self.locale['object'][kw['object']].format()

Here we used ``locale`` attribute of message object to get access to parent 
locale.  Locale's method ``__getitem__`` returns catalog object.  Catalog's
method ``__getitem__`` returns message.  Method ``format`` of message object
returns formatted translation string.  So, this:

..  code-block:: python

    self.locale['object']['article'].format()

Is equal to:

..  code-block:: python

    t.translate('object:article', u'Article')

Let's do the same thing in Russian.  Take notice, Russian have other rules than
English.  We can't simply substitute object name into translation string of 
``message:removed``.  Verb "удалять" (to remove) should be inflected according
noun's gender, which represent object name.  There are three noun's gender in
Russian: ......  So, we need ........ during translation.

..  code-block:: python

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

    print t.translate('message:removed', 'Object has been removed', object='article')
    print t.translate('message:removed', 'Object has been removed', object='comment')

    t.lang = 'ru'
    print t.translate('message:removed', 'Object has been removed', object='article')
    print t.translate('message:removed', 'Object has been removed', object='comment')

Here we added ``gender`` attribute to the messages from ``object`` catalog, and
use this attribute on translation ``message:removed`` to select appropriate 
translation string.  The best explanation, how it works, is a source code of 
``Message.format`` method:

..  code-block:: python

    def format(self, **kw):
        params = self.defaults.copy()
        params.update(kw)
        if self.filter:
            self.filter(self, params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)


Using helpers
-------------

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