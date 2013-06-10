import sys


version = sys.version_info[0]

if version == 3:
    strtypes = str
    unicode = str
else:
    strtypes = (str, unicode)
    unicode = unicode
