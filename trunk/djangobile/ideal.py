# -*- coding: utf-8 -*-
from xml.dom import minidom

from django.template.loader import get_template_from_string, get_template, render_to_string


class Ideal(object):
    def __init__(self, source, origin=None, name=None):
        self.source = source.encode("utf-8")

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

    def namespace(self, node_name):
        return "%s:%s" % (self.document.prefix, node_name)

    def render(self, context):
        body = self.doc.getElementsByTagNameNS(self.ns, 'body')[0]
        self.data['body'] = minidom.Element('body')
        for child_node in body.childNodes:
            self._resolve(self.data['body'], child_node, context)
        self.data['body'] = self.data['body'].toprettyxml()
        return render_to_string('generic_xhtml.html', self.data, context)

    def _resolve(self, parent_node, child_node, context=None):
        if child_node.nodeName == self.namespace('p'):
            _parent_node = minidom.Element('p')
        elif child_node.nodeName == self.namespace('label'):
            _parent_node = minidom.Element('label')
        else:
            _parent_node = minidom.Element(child_node.nodeName)
        for _child_node in child_node.childNodes:
            self._resolve(_parent_node, _child_node, context)
        parent_node.appendChild(_parent_node)

    def entryfield(self):
        pass
