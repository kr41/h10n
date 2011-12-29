from nose import tools

from h10n.helper.pluralize import Pluralize


def test():
    pluralize = Pluralize('en', None)
    tools.eq_(pluralize(1), 0)
    tools.eq_(pluralize(2), 1)
