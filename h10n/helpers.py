class GenericHelpers(object):
    """ Generic Helpers """

    def message(self, locale, id, **params):
        """ Format specified message from current locale """
        return locale[id].format(**params)
