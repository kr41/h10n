from h10n.server.catalog import Catalog
from h10n.server.message import Message
from h10n.exception import keep_context
from h10n.exception import NamedContext
from h10n.exception import Context


class Locale(object):

    def __init__(self, name, catalogs):
        self.name = name
        try:
            self.lang, self.country = name.split('-')
            self.catalogs = {'__prototype__': Message(locale=self)}
            for catalog_name, catalog in catalogs.iteritems():
                try:
                    if catalog_name in self.catalogs:
                        raise ValueError(
                            'Duplicate catalog name "{0}": {1}'.format(
                                catalog_name, repr(catalog)
                            )
                        )
                    self.catalogs[catalog_name] = Catalog(name=catalog_name,
                                                          locale=self,
                                                          **catalog)
                except Exception, e:
                    Context.extend(e, NamedContext('Catalog', catalog_name))
        except Exception, e:
            Context.extend(e, NamedContext('Locale', name))

    def __repr__(self):
        return '<Locale: {0}>'.format(self.name)

    @keep_context()
    def __getitem__(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.catalogs[name][tail]
        return self.catalogs[name]

    def get_helper(self, name):
        pass
