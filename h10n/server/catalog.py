from h10n.server.message import Message
from h10n.exception import keep_context
from h10n.exception import NamedContext
from h10n.exception import Context


class Catalog(object):
    """ Message Catalog """

    def __init__(self, name, locale, source, strategy=None):
        self.name = name
        try:
            self.locale = locale
            # Detect strategy if no provided one
            if strategy is None:
                if hasattr(source, 'strategy'):
                    strategy = source.strategy
            # Compile messages on demand...
            if strategy == 'on_demand':
                self.source = source
            # ...or on start-up and store compiled ones in memory
            elif strategy == 'on_start_up':
                self.source = {}
                for message in source:
                    id = message['id']
                    try:
                        if id in self.source:
                            raise ValueError(
                                'Duplicate message id "{0}": {1}'.format(
                                    id, message
                                )
                            )
                        self.source[id] = self._compile_message(**message)
                    except Exception, e:
                        Context.extend(
                            e,
                            NamedContext(e, NamedContext('Message', id))
                        )
            else:
                raise ValueError('Invalid strategy "{0}"'.format(strategy))
        except Exception, e:
            Context.extend(e, NamedContext('Catalog', name))

    def __repr__(self):
        return '<Catalog: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, id):
        result = self.source[id]
        # If result is not compiled message, i.e. strategy == 'on_demand'
        if not isinstance(result, Message):
            result['id'] = id
            result = self._compile_message(**result)
        return result

    @keep_context()
    def _compile_message(self, prototype='__prototype__', **message):
        prototype = self.locale[prototype]
        return prototype.clone(**message)
