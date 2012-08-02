..  _debugging:

Debugging
=========

The main idea of h10n is broken translation can't break application.  This means
that any exception, occurred during translation is swallowed by Translator.
Translator use standard ``logging`` package to log debug info.  So, let's run
following code:

..  literalinclude:: ../_static/examples/6_debugging/app.py
    :language: python

An output will be::

    DEBUG:h10n.translator:Translate ru-RU:test:error
    ERROR:h10n.translator:Translation error ru-RU:test:error
    Traceback (most recent call last):
        ...
    KeyError: ('test', <ExceptionContext: [<Locale: ru-RU>]>)
    DEBUG:h10n.translator:Fallback to en-GB
    ERROR:h10n.translator:Translation error en-GB:test:error
    Traceback (most recent call last):
        ...
    KeyError: ('error', <ExceptionContext: [<Locale: en-GB>, <Catalog: test>]>)
    DEBUG:h10n.translator:Fallback to en-US
    ERROR:h10n.translator:Translation error en-US:test:error
    Traceback (most recent call last):
        ...
    Exception: ('Raised from filter', <ExceptionContext: [<Message: error>]>)

First of all, assertion passed.  So, our program is not broken, Translator used
fallback message (second parameter passed
to :meth:`h10n.translator.Translator.translate` method).

In the log you can see three debug messages and three error ones with exception
tracebacks.  The most interesting thing is a second argument of exception.
It is an instance of :class:`h10n.util.ExceptionContext`, which stores
"breadcrumbs" to the problem.

First exception raised from ``ru-RU`` locale, because it doesn't contain
``test`` catalog.  Second one raised from ``en-GB:test`` catalog, because it
doesn't contain ``error`` message.  Third one raised from filter of message
``en-US:test:error``.

Take a notice to fallback order.  After fail in ``ru-RU`` locale Translator used
``en-GB`` one, because it specified in ``fallback`` parameter of Translator
constructor explicitly.  After fail in ``en-GB`` locale Translator used
``en-US`` one, because it is default locale.  And finally, Translator used
fallback message passed to :meth:`h10n.translator.Translator.translate` method.
