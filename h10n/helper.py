class HelperManager(object):

    def __init__(self, locale_manager):
        self.lm = locale_manager

    def bind_helper(self, namespace, helper):
        setattr(self, namespace, helper)
        helper.bind(self.lm)
