class h10nException(Exception):
    """ Base h10n Exception """

class NotConfigured(h10nException):
    """ Raised on attempt to use unconfigured Locale Manager """
