# -*- coding: utf-8 -*-


class Ideal(object):
    def __init__(self, source, origin=None, name=None):
        self.source = source

    def render(self, context):
        print "context: %s" % context.get('HTTP_USER_AGENT', None)
        return self.source
