from h10n.server.locale import Locale


class Server(object):

    def __init__(self, locales):
        self.locales = {}
        for name, locale in locales.iteritems():
            self.locales[name] = Locale(name=name, **locale)

    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.locales[name][tail]
        return self.locales[name]
