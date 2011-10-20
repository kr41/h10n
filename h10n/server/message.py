""" Message Module

Provides function to build Localized Messages.
"""

class Message(object):
    """ Localized Message """

    def __init__(self, locale, id='__prototype__'):
        self.id = id
        self.fullname = '{0}.{1}'.format(locale.name, id)
        self.locale = locale
        self.key = None
        self.msg = None
        self.defaults = {}
        self.filters = []

    def __repr__(self):
        return '<Message: {0}>'.format(self.fullname)

    def clone(self, id, key=None, msg=None, defaults=None, filters=None):
        try:
            result = self.__class__(self.locale, id)
            result.key = key or self.key
            result.msg = msg or self.msg
            result.defaults.update(self.defaults)
            result.defaults.update(defaults or {})
            result.filters = self._compile_filters(filters or [])
            return result
        except Exception, e:
            e.args = e.args + (repr(result),)
            raise

    def format(self, **kw):
        """ Format Message according to passed parameters """
        params = self.defaults.copy()
        params.update(kw)
        for filter in self.filters:
            filter(params)
        msg = self.msg
        if self.key is not None:
            key = self.key.format(**params)
            msg = msg[key]
        return msg.format(**params)

    _filter_template = 'def f(kw): ({output}) = helper(self.locale, {input})'

    def _compile_filters(self, filters):
        """ Setup Filters """
        result = []
        # Copy prototype's filters at the begin of filter chain
        # if no directive provided
        if not ('__no_prototype__' in filters or '__prototype__' in filters):
            result.extend(self.filters)
        for definition in filters:
            # Process directives
            if isinstance(definition, basestring):
                if definition == '__prototype__':
                    result.extend(self.filters)
                continue
            # Compile filter
            helper_name, input, output = definition
            try:
                helper = self.locale.get_helper(helper_name)
                input = self._map(input)
                output = self._map(output)
                code = self._filter_template.format(input=input, output=output)
                exec code in locals()
                result.append(f)
            except Exception, e:
                e.args = e.args + ('<Filter: {0}>'.format(helper_name),)
                raise
        return result

    def _map(self, map):
        """ Map Converter

        Converts map into Python code fragment, that will be used to construct
        filter source code.
        """
        if hasattr(map, 'keys'):
            # When map is dict-like object
            kw = map
            args = kw.pop('*', [])
            if not hasattr(args, '__iter__'):
                args = [args]
        elif hasattr(map, '__iter__'):
            # When map is list-like object
            args = map
            kw = {}
        else:
            # When map is not iterable
            args = [map]
            kw = {}
        result = [self._value(arg) for arg in args]
        result.extend('{0}={1}'.format(name, self._value(arg))
                      for name, arg in kw.iteritems())
        result = ', '.join(result)
        return result

    def _value(self, value):
        """ Value converter

        Converts value into Python code fragment, that will be used to construct
        map source code.
        """
        if isinstance(value, basestring) and '{' in value:
            value = value.replace('{', 'kw["').replace('}', '"]')
        else:
            value = repr(value)
        return value
