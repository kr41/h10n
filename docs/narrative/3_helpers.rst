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

..  literalinclude:: ../_static/examples/3_helpers/app.py
    :language: python

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
