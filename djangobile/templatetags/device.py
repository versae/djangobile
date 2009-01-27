# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import Node, Library, TemplateSyntaxError

from djangobile.utils import get_device_template_paths

register = Library()

if hasattr(settings, 'DEVICE_MEDIA_URL_TAG_PREFIX'):
    tag_prefix = getattr(settings, 'DEVICE_MEDIA_URL_TAG_PREFIX')
    if not tag_prefix:
        tag_prefix = ''
    else:
        tag_prefix = "%s_" % tag_prefix
else:
    tag_prefix = 'device_'


class DeviceMediaUrlNode(Node):
    def __init__(self, file_path=None):
        self.file_path = file_path

    def render(self, context):
        device = context.get('device', None)
        if '__MEDIA_URL' in context:
            media_url = context.get('__MEDIA_URL', None)
        else:
            media_url = context.get('MEDIA_URL', None)
        if device:
            media_paths = get_device_template_paths(device, self.file_path)
            load_name = self.source[0].loadname
            if '/' in load_name:
                device_criteria = load_name.split('/')[0]
                media_path = "%s/%s" % (device_criteria, self.file_path)
                if media_path in media_paths:
                    return "%s%s" % (media_url, media_path)
            return "%s%s" % (media_url, self.file_path)
        else:
            return "%s%s" % (media_url, self.file_path)


class OverrideMediaUrlNode(Node):
    def render(self, context):
        device = context.get('device', None)
        media_url = context.get('MEDIA_URL', None)
        if device:
            media_paths = get_device_template_paths(device, '')
            load_name = self.source[0].loadname
            if '/' in load_name:
                device_criteria = load_name.split('/')[0]
                media_path = "%s/" % (device_criteria)
                if media_path in media_paths:
                    if not '__MEDIA_URL' in context:
                        context['__MEDIA_URL'] = context['MEDIA_URL']
                    context['MEDIA_URL'] = "%s%s" % (media_url, media_path)
        return ''


def do_device_media_url(parser, token):
    """
    Return a aboslute URL for media file in a aware device context.
    If device media URL not exists for that device, MEDIA_URL is inserted.

    Example::

        <link rel="stylesheet" type="text/css" href="{% device_media_url "css/style.css" %}" />
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "%r tag takes one argument: the path to media file" % bits[0]
    path = bits[1]
    if path[0] in ('"', "'") and path[-1] == path[0]:
        return DeviceMediaUrlNode(path[1:-1])
    return DeviceMediaUrlNode(bits[1])


def do_override_media_url(parser, token):
    """
    Override MEDIA_URL value with path according to device detection.

    Example::

        {% override_media_url %}
    """
    bits = token.contents.split()
    if len(bits) != 1:
        raise TemplateSyntaxError, "%r tag takes no argument" % bits[0]
    return OverrideMediaUrlNode()


register.tag('%smedia_url' % tag_prefix, do_device_media_url)
register.tag('override_media_url', do_override_media_url)
