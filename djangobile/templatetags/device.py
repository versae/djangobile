# -*- coding: utf-8 -*-
from os import path

from django.conf import settings
from django.template import Node, Library, Variable, TemplateSyntaxError

from djangobile.utils import (get_device_template_paths,
                              parse_args_kwargs_and_as_var)

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
    def __init__(self, file_path=None, force_detection=False):
        self.file_path = file_path
        self.force_detection = force_detection

    def render(self, context):
        if isinstance(self.file_path, Variable):
            file_path = self.file_path.resolve(context)
        else:
            file_path = self.file_path
        device = context.get('device', None)
        if '__MEDIA_URL' in context:
            media_url = context.get('__MEDIA_URL', None)
        else:
            media_url = context.get('MEDIA_URL', None)
        if device:
            media_paths = get_device_template_paths(device, file_path)
            if self.force_detection:
                for media_path in media_paths:
                    media_path_split = media_path.split("/")
                    aboslute_media_path = path.join(settings.MEDIA_ROOT,
                                                    *media_path_split)
                    if path.isfile(aboslute_media_path):
                        return "%s%s" % (media_url, media_path)
            load_name = self.source[0].loadname
            if '/' in load_name:
                device_criteria = load_name.split('/')[0]
                media_path = "%s/%s" % (device_criteria, file_path)
                if media_path in media_paths:
                    return "%s%s" % (media_url, media_path)
        return "%s%s" % (media_url, file_path)


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
    Return a absolute URL for media file in a aware device context.
    If device media URL not exists for that device, MEDIA_URL is inserted.
    The optional argument force_detection is True if media file exists, in
    which case it's returned.

    Example::

        <link rel="stylesheet" type="text/css" href="{% device_media_url "css/style.css" %}" />
    """
    args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, token)
    return DeviceMediaUrlNode(*args, **kwargs)


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
