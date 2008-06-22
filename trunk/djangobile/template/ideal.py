# -*- coding: utf-8 -*-
from xml.dom import minidom

from django.template import Variable
from django.template.loader import render_to_string

EXPRESSION_LANGUAGE_TAG_START = '${'
EXPRESSION_LANGUAGE_TAG_END = '}'


class MalformedIdealTemplateException(Exception):
    pass


class GenericXhtml(object):
    def __init__(self, source, namespace="http://morfeo-project.org/mymobileweb"):
        self.source = source
        self.namespace = namespace
        self.doc = minidom.parseString(source)
        self.document = self.doc.getElementsByTagNameNS(self.namespace, 'document')[0]
        self.data = {}
        self._load_initial_data()

    def _load_initial_data(self):
        title = self.doc.getElementsByTagNameNS(self.namespace, 'title')[0]
        self.data['title'] = title.firstChild.data

    def _resolve(self, parent_node, node, context=None):
        tags = ('action', 'anchor', 'br', 'chainedmenu', 'datefield', 'div', \
                'entryfield', 'hr', 'image', 'include', 'item', 'label', 'link', \
                'list', 'menu', 'object', 'option', 'p', 'panel', 'phonebookadder', \
                'reset', 'select', 'submit', 'table', 'td', 'telephonecaller', \
                'textarea', 'textblock', 'th', 'timefield', 'tr', 'upload')
        new_node = None
        tag_name = self._tag_name(node.nodeName)
        if tag_name in tags:
            callable_tag = getattr(self, "%s_tag" % tag_name, None)
            if callable(callable_tag):
                new_node = callable_tag(node=node, context=context)
        if node.nodeType == 3: # Text node
            new_node = self.doc.createTextNode(node.data)
        if not new_node:
            new_node = minidom.Element(node.nodeName)
        for child_node in node.childNodes:
            self._resolve(new_node, child_node, context)
        parent_node.appendChild(new_node)

    def _tag_name(self, node_name):
        if self.document.prefix in node_name:
            ns_len = len(self.document.prefix)
            return node_name[ns_len+1:]
        return node_name

    def _expression_language(self, value):
        el_tag_start_len = len(EXPRESSION_LANGUAGE_TAG_START)
        el_tag_end_len = len(EXPRESSION_LANGUAGE_TAG_END)
        if len(value) > (el_tag_start_len + el_tag_end_len):
            if value[:el_tag_start_len] == EXPRESSION_LANGUAGE_TAG_START and \
            value[-el_tag_end_len:] == EXPRESSION_LANGUAGE_TAG_END:
                return value[el_tag_start_len:-el_tag_end_len]
        return

    def ns(self, node_name):
        return "%s:%s" % (self.document.prefix, node_name)

    def render(self, context):
        body = self.doc.getElementsByTagNameNS(self.namespace, 'body')[0]
        self.data['body'] = minidom.Element('body')
        for child_node in body.childNodes:
            self._resolve(self.data['body'], child_node, context)
        self.data['body'] = self.data['body'].toprettyxml()
        return render_to_string('generic_xhtml.html', self.data, context)

    def action_tag(self, *args, **kwargs):
        context = kwargs.get('context', None)
        node = kwargs.get('node', None)
        tag = minidom.Element('a')
        return tag

    def br_tag(self, *args, **kwargs):
        context = kwargs.get('context', None)
        node = kwargs.get('node', None)
        tag = minidom.Element('br')
        return tag

    def hr_tag(self, *args, **kwargs):
        context = kwargs.get('context', None)
        node = kwargs.get('node', None)
        tag = minidom.Element('hr')
        return tag

    def p_tag(self, *args, **kwargs):
        context = kwargs.get('context', None)
        node = kwargs.get('node', None)
        tag = minidom.Element('p')
        return tag

    def label_tag(self, *args, **kwargs):
        context = kwargs.get('context', None)
        node = kwargs.get('node', None)
        tag = minidom.Element('label')
        return tag

    def entryfield_tag(self, *args, **kwargs):
        context = kwargs.get('context', None)
        node = kwargs.get('node', None)
        tag = minidom.Element('input')
        if node:
            tag.setAttribute('type', 'text')
            bind = node.getAttribute('bind')
            el = self._expression_language(bind)
            if el:
                bind = Variable(el).resolve(context)
        tag.setAttribute('value', bind)
        return tag


class HtmlWeb(GenericXhtml):
    pass


class GenericIMode(GenericXhtml):
    pass


class IMode(GenericXhtml):
    pass


class OmaXhtmlMp(GenericXhtml):
    pass


class W3Xhtml(GenericXhtml):
    pass


class Wml(GenericXhtml):
    pass

