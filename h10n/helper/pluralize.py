class Pluralize(object):

    def __init__(self, lang, region):
        self._call = getattr(self, lang)

    def __call__(self, count):
        return self._call(count)

    def en(self, count):
        return 0 if count == 1 else 1
