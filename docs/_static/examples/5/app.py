# app.py

import os

from h10n import Translator

path = os.path.join(os.path.dirname(__file__), 'translations')
t = Translator(scan='path://' + path, default='en-US')

print t.translate('message:choose', 'Choose an object', object='article')
print t.translate('message:choose', 'Choose an object', object='comment')
print t.translate('message:removed', 'Object successfully removed',
                  object='article')
print t.translate('message:removed', 'Object successfully removed',
                  object='comment')

t.lang = 'ru'
print t.translate('message:choose', 'Choose an object', object='article')
print t.translate('message:choose', 'Choose an object', object='comment')
print t.translate('message:removed', 'Object successfully removed',
                  object='article')
print t.translate('message:removed', 'Object successfully removed',
                  object='comment')
