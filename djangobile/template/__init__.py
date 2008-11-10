# -*- coding: utf-8 -*-
from inspect import getargspec
from django.conf import settings
from django.template import Node, Variable, generic_tag_compiler
from django.template.context import Context
from django.utils.itercompat import is_iterable
from django.utils.functional import curry
from django.utils.html import escape

from django.template import Library as DjangoLibrary


class Library(DjangoLibrary):
    def inclusion_tag(self, file_name, context_class=Context, takes_context=False):
        def dec(func):
            params, xx, xxx, defaults = getargspec(func)
            if takes_context:
                if params[0] == 'context':
                    params = params[1:]
                else:
                    raise TemplateSyntaxError("Any tag function decorated with takes_context=True must have a first argument of 'context'")

            class InclusionNode(Node):
                def __init__(self, vars_to_resolve):
                    self.vars_to_resolve = map(Variable, vars_to_resolve)

                def render(self, context):
                    resolved_vars = [var.resolve(context) for var in self.vars_to_resolve]
                    if takes_context:
                        args = [context] + resolved_vars
                    else:
                        args = resolved_vars

                    dict = func(*args)

                    if not getattr(self, 'nodelist', False):
                        from djangobile.template.loader import get_template, select_template
                        device = getattr(context.get('request', None), 'device', None)
                        if device:
                            args = (file_name, device)
                        else:
                            args = (file_name, )
                        if not isinstance(file_name, basestring) and is_iterable(file_name):
                            t = select_template(*args)
                        else:
                            t = get_template(*args)
                        self.nodelist = t.nodelist
                    return self.nodelist.render(context_class(dict,
                            autoescape=context.autoescape))

            compile_func = curry(generic_tag_compiler, params, defaults, getattr(func, "_decorated_function", func).__name__, InclusionNode)
            compile_func.__doc__ = func.__doc__
            self.tag(getattr(func, "_decorated_function", func).__name__, compile_func)
            return func
        return dec


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
        preferred_markup = device.get('preferred_markup').lower()
        if preferred_markup in ('html_web_3_2', 'html_web_4_0'):
            from djangobile.template.ideal import HtmlWeb as Processor
        elif preferred_markup in ('html_wi_imode_compact_generic', ):
            from djangobile.template.ideal import GenericIMode as Processor
        elif preferred_markup in ('html_wi_imode_html_1', 'html_wi_imode_html_2', \
                                  'html_wi_imode_html_3', 'html_wi_imode_html_4', \
                                  'html_wi_imode_html_5'):
            from djangobile.template.ideal import IMode as Processor
        elif preferred_markup in ('html_wi_oma_xhtmlmp_1_0', ):
            from djangobile.template.ideal import OmaXhtmlMp as Processor
        elif preferred_markup in ('html_wi_w3_xhtmlbasic', ):
            from djangobile.template.ideal import W3Xhtml as Processor
        elif preferred_markup in ('wml_1_1', 'wml_1_2', 'wml_1_3'):
            from djangobile.template.ideal import Wml as Processor
        else:
            from djangobile.template.ideal import GenericXhtml as Processor
        processor = Processor(self.source)
        return processor.render(context)
