..  _glossary:

Glossary
========

..  glossary::
    :sorted:

    translator
        Translator is an object to manage :term:`locales<locale>` and perform
        :term:`message` translation.
        See the :class:`h10n.translator.Translator` class for details.

    locale
        Locale is an object which stores :term:`messages<message>` and
        application-level :term:`helpers<helper>`.  Locale is
        uniquely identified by its name -- the string in format ``xx-YY``,
        where ``xx`` is language identifier and ``YY`` is country one.  Note,
        locale name is **case-sensitive**.

    catalog
        Translation catalog or domain is a logical group
        of :term:`messages<message>` of the particular :term:`locale`.
        Usually, represented by particular file.  In the h10n, catalog objects
        are used to store messages and :term:`filter`-level
        :term:`helpers<helper>`.

    message
        Message is a string, which should be translated into different
        :term:`locales<locale>`.  Messages are instanced from class
        :class:`h10n.core.Message` and stored in the :term:`catalogs<catalog>`.

    filter
        Is a Python callable object, which transforms input parameters before
        formatting :term:`message`.

    helper
        Helper is a Python callable object, which provides utility functional,
        such as performing pluralization, formatting dates, etc.
        Helpers are stored in :term:`helper namespace`.

    helper namespace
        Helper namespace is an object, which stores particular
        :term:`helpers<helper>` under specified aliases.  Is used in
        the :term:`translator` for application level helpers and in
        the :term:`catalogs<catalog>` for :term:`filter` level ones.

    helper factory
        Helper factory is a Python callable object, which returns :term:`helper`
        for particular :term:`locale`.
