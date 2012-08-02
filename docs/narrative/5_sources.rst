Sources
=======

In previous topics we define messages directly in source code.  But in real
application you will place it in separate files.  Let's see how to do it.

Files listed below are available
in the `examples directory <../_static/examples/5_sources/>`_::

    /                                       # Sample application root directory
        translations/                       # Translations directory
            en-US/                          # "en-US" locale
                object.yaml                 # "object" catalog
                message.yaml                # "message" catalog
            ru-RU/                          # "ru-RU" locale
                proto.yaml                  # "proto" catalog
                object.yaml                 # "object" catalog
                message.yaml                # "message" catalog
        helpers.py                          # Helpers module
        app.py                              # Application itself


..  literalinclude:: ../_static/examples/5_sources/translations/en-US/object.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5_sources/translations/en-US/message.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5_sources/translations/ru-RU/proto.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5_sources/translations/ru-RU/object.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5_sources/translations/ru-RU/message.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5_sources/helpers.py
    :language: python

..  literalinclude:: ../_static/examples/5_sources/app.py
    :language: python


Take a notice to ``scan`` parameter passed to Translator.  It replaced
``locales`` one.  See :mod:`h10n.source` module doc-strings for details.
