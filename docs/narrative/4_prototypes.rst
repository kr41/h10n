Prototypes
==========

Let's add ``message:choose`` to Russian locale.

..  literalinclude:: ../_static/examples/4_prototypes/app_1.py
    :language: python


Take a notice, nouns in Russian version of the message ``message:choose`` is
used in accusative case instead of nominative one.  So, we added appropriate
forms to ``object:article`` and ``object:comment``.  Also, we added default
value ``n`` (nominative) for ``case`` parameter.  Obviously, there is a
copy-paste work to add ``defaults`` and ``key`` parameters to each noun
in Russian locale.  Let's use prototype instead.


..  literalinclude:: ../_static/examples/4_prototypes/app_2.py
    :language: python
