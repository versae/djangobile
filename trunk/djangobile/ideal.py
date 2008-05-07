# -*- coding: utf-8 -*-
import xml.dom.minidom
from xml.dom.minidom import Node


class Ideal(object):
    def __init__(self, source, origin=None, name=None):
        self.source = source

    def render(self, context=None, cls=None):
        if not context:
            return self.source
        device = context.get('device')
        if cls:
            processor = cls(self.source)
            return processor.render(context)
        fall_back = device.get('fall_back').lower()
        if fall_back in ('generic', 'generic_xhtml'):
            processor = GenericXhtml(self.source)
        else:
            return self.source
        return processor.render(context)


class GenericXhtml(object):
    def __init__(self, source, namespace="http://morfeo-project.org/mymobileweb"):
        self.source = source
        self.doc = xml.dom.minidom.parseString(source)
        self.document = self.doc.getElementsByTagNameNS(namespace, 'document')[0]

    def ns(self, node):
        return "%s:%s" % (self.document.prefix, node)

    def render(self, context):
        return self.source

    def entryfield(self):
        pass
