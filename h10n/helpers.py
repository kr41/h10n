""" Generic Helpers """

def message(locale, id, **params):
    """ Format specified message from current locale """
    return locale[id].format(**params)
