Filters
=======

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
    Article has been successfully removed
    Comment has been successfully removed

There are two interesting things.  Let's start from last one.  We don't added
catalog ``message`` into Russian locale.  So, translator used English locale as 
fallback one to translate wrong Russian messages.  It also logged debug 
information, but it failed with message "No handlers could be found for logger 
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
to noun's gender, which represent object name.  There are three noun's gender in
Russian: masculine, feminine and neuter.

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
