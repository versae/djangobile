# -*- coding: utf-8 -*-
from xml.dom import minidom

from django.template.loader import get_template_from_string, get_template, render_to_string


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
        self.ns = namespace
        self.doc = minidom.parseString(source)
        self.document = self.doc.getElementsByTagNameNS(self.ns, 'document')[0]
        self.data = {}
        self.__load_initial_data__()

    def __load_initial_data__(self):
        title = self.doc.getElementsByTagNameNS(self.ns, 'title')[0]
        self.data['title'] = title.firstChild.data

    def ns(self, node):
        return "%s:%s" % (self.document.prefix, node)

    def render(self, context):
        return render_to_string('generic_xhtml.html', self.data, context)

    def entryfield(self):
        pass
