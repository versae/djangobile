from django.template import TemplateSyntaxError, TemplateDoesNotExist, Variable
from django.template import Library
from django.template.loader import get_template_from_string, find_template_source
from django.template.loader_tags import ExtendsNode, IncludeNode, ConstantIncludeNode
from django.conf import settings

from djangobile.template.loader import get_template
from djangobile.utils import (get_device_template_paths,
                              parse_args_kwargs_and_as_var,
                              template_log)

register = Library()

if hasattr(settings, 'DEVICE_LOADER_TAGS_PREFIX'):
    tag_prefix = getattr(settings, 'DEVICE_LOADER_TAGS_PREFIX')
    if not tag_prefix:
        tag_prefix = node_prefix = ''
    else:
        if len(tag_prefix) > 1:
            node_prefix = "%s%s" % (tag_prefix[:1].upper(), tag_prefix[1:])
        else:
            node_prefix = tag_prefix.upper()
        tag_prefix = "%s_" % tag_prefix
else:
    tag_prefix = 'device_'
    node_prefix = 'Device'


class DeviceExtendsNode(ExtendsNode):
    def __repr__(self):
        if self.parent_name_expr:
            return "<%sExtendsNode: extends %s>" % (node_prefix, self.parent_name_expr.token)
        return '<%sExtendsNode: extends "%s">' % (node_prefix, self.parent_name)

    def get_parent(self, context):
        if self.parent_name_expr:
            self.parent_name = self.parent_name_expr.resolve(context)
        parent = self.parent_name
        if not parent:
            error_msg = "Invalid template name in 'extends' tag: %r." % parent
            if self.parent_name_expr:
                error_msg += " Got this from the '%s' variable." % self.parent_name_expr.token
            raise TemplateSyntaxError, error_msg
        if hasattr(parent, 'render'):
            return parent # parent is a Template object
        exceptions_list = []
        source, origin = None, None
        device = context.get('device', None)
        if device:
            device_path_list = get_device_template_paths(device, parent)
            for device_path in device_path_list:
                try:
                    source, origin = find_template_source(device_path)
                except TemplateDoesNotExist:
                    exceptions_list.append(device_path)
                if source:
                    template_log(device_path, log="extends")
                    break
        if not source:
            try:
                source, origin = find_template_source(parent)
                template_log(parent, log="extends")
            except TemplateDoesNotExist:
                exceptions_list.append(parent)
                raise TemplateSyntaxError, "Template (%s) cannot be extended, because it doesn't exist" % ", ".join(exceptions_list)
        return get_template_from_string(source, origin, parent)


class DeviceConstantIncludeNode(ConstantIncludeNode):
    def __init__(self, template_path):
        self.template_path = template_path

    def render(self, context):
        device = context.get('device', None)
        try:
            t = get_template(self.template_path, device, log="include")
            self.template = t
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            self.template = None
        if self.template:
            return self.template.render(context)
        else:
            return ''


class DeviceIncludeNode(IncludeNode):
    def render(self, context):
        device = context.get('device', None)
        try:
            template_name = self.template_name.resolve(context)
            t = get_template(template_name, device, log="include")
            return t.render(context)
        except TemplateSyntaxError, e:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''
        except:
            return '' # Fail silently for invalid included templates.


def do_device_extends(parser, token):
    """
    Signal that this template extends a parent template.
    Allows an optional auto_detection parameter; if it's False, its behavour is
    like native extends templatetag.

    This tag may be used in two ways: ``{% extends "base" %}`` (with quotes)
    uses the literal value "base" as the name of the parent template to extend,
    or ``{% extends variable %}`` uses the value of ``variable`` as either the
    name of the parent template to extend (if it evaluates to a string) or as
    the parent tempate itelf (if it evaluates to a Template object).
    """
    args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, token)
    auto_detection = kwargs.get('auto_detection', True)
    bits = token.contents.split()
    if len(bits) > 3:
        raise TemplateSyntaxError, "'%s' takes at most two argument" % bits[0]
    parent_name, parent_name_expr = None, None
    if bits[1][0] in ('"', "'") and bits[1][-1] == bits[1][0]:
        parent_name = bits[1][1:-1]
    else:
        parent_name_expr = parser.compile_filter(bits[1])
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(DeviceExtendsNode):
        raise TemplateSyntaxError, "'%s' cannot appear more than once in the same template" % bits[0]
    if auto_detection:
        return DeviceExtendsNode(nodelist, parent_name, parent_name_expr)
    else:
        return ExtendsNode(nodelist, parent_name, parent_name_expr)


def do_device_include(parser, token):
    """
    Load a template and renders it with the current context.
    Allows an optional auto_detection parameter; if it's False, its behavour is
    like native extends templatetag.

    Example::

        {% include "foo/some_include" %}
    """
    args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, token)
    auto_detection = kwargs.get('auto_detection', True)
    bits = token.contents.split()
    if len(bits) > 3:
        raise TemplateSyntaxError, "%r tag takes one argument: the name of the template to be included" % bits[0]
    path = bits[1]
    if path[0] in ('"', "'") and path[-1] == path[0]:
        if auto_detection:
            return DeviceConstantIncludeNode(path[1:-1])
        else:
            return ConstantIncludeNode(path[1:-1])
    if auto_detection:
        return DeviceIncludeNode(bits[1])
    else:
        return IncludeNode(bits[1])


register.tag('%sextends' % tag_prefix, do_device_extends)
register.tag('%sinclude' % tag_prefix, do_device_include)
