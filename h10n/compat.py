import sys

version = sys.version_info[0]

if version == 3:
    import collections

    strtypes = str
    unicode = str

    def callable(f):
        return isinstance(f, collections.Callable)

    def u(s):
        return s
else:
    strtypes = (str, unicode)

    unicode = unicode

    def u(s):
        return s.decode('utf-8')
