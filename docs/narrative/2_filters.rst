Filters
=======

Let's go ahead and add to our application message template.

..  literalinclude:: ../_static/examples/2/app_1.py
    :language: python

There are two interesting things.  Let's start from last one.  We don't added
catalog ``message`` into Russian locale.  So, translator used English (default)
locale as fallback one to translate wrong Russian messages.  It also logged
debug information, but it failed with message "No handlers could be found for
logger "h10n.translator" (this message will fired to ``stderr`` if you run this
program), because we didn't configure logger.  We will do it later, on learning
h10n :ref:`debugging`.

Most interesting thing is ``message:removed`` translation message, which is
defined using full form of definition.  The best way to show difference between
full and simple forms is to look on how message object is constructed.  If you
look into sources of :class:`h10n.core.Catalog`, which constructs
:class:`h10n.core.Message` objects from definitions, you will see, that it's
little bit complex than this:

..  code-block:: python

    if isinstance(message, basestring):
        message = {'msg': message}
    message = Message(**message)

A translation string is provided via ``msg`` keyword argument.  Other keyword
argument is ``filter`` one.  Filter is just Python code with little pinch of
syntax sugar.  Filter makes all dirty work on translation.  How it work?
Method ``translate`` of translator object accepts keyword arguments.  When it
find specified message, it call message's :meth:`h10n.core.Message.format`
method passing these arguments.  Method ``format`` process provided arguments
using filter and calls ``format`` method of translation string ``msg``,
using filtered arguments.

So, string::

    $object = self.locale['object'][$object].format()

Becomes a function, which accept message object as first argument and dict of
keyword arguments as second one:

..  code-block:: python

    def filter(self, kw):
        kw['object'] = self.locale['object'][kw['object']].format()

Here we used ``locale`` attribute of message object to get access to parent
locale.  Method ``__getitem__`` of :class:`h10n.core.Locale` returns catalog
object.  Method ``__getitem__`` of :class:`h10n.core.Catalog` returns message.
Method ``format`` of message object returns formatted translation string.
So, this:

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

..  literalinclude:: ../_static/examples/2/app_2.py
    :language: python

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
