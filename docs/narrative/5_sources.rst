Sources
=======

In previous topics we define messages directly in source code.  But in real
application you will place it in separate files.  Let's see how to do it::

    sample/                                 # Sample application root directory
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


..  literalinclude:: ../_static/examples/5/translations/en-US/object.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5/translations/en-US/message.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5/translations/ru-RU/proto.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5/translations/ru-RU/object.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5/translations/ru-RU/message.yaml
    :language: yaml

..  literalinclude:: ../_static/examples/5/helpers.py
    :language: python

..  literalinclude:: ../_static/examples/5/app.py
    :language: python


Take a notice to ``scan`` parameter passed to Translator...
