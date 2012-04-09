Basic translation
=================

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