# -*- coding: utf-8 -*-
from os import path

from django.conf import settings
from django.template import Node, Library, Variable, TemplateSyntaxError

from djangobile.utils import (get_device_template_paths, get_device_directories,
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


#################
# Template tags #
#################

class DeviceMediaUrlNode(Node):
    def __init__(self, file_path=None):
        self.file_path = file_path

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
            for media_path in media_paths:
                media_path_split = media_path.split("/")
                aboslute_media_path = path.join(settings.MEDIA_ROOT,
                                                *media_path_split)
                if path.isfile(aboslute_media_path):
                    return "%s%s" % (media_url, media_path)
        return "%s%s" % (media_url, file_path)


class OverrideMediaUrlNode(Node):
    def render(self, context):
        device = context.get('device', None)
        media_url = context.get('MEDIA_URL', None)
        if device:
            media_paths = get_device_directories(device)
            for media_path in media_paths:
                aboslute_media_path = path.join(settings.MEDIA_ROOT, media_path)
                if path.isdir(aboslute_media_path):
                    if not '__MEDIA_URL' in context:
                        context['__MEDIA_URL'] = context['MEDIA_URL']
                    context['MEDIA_URL'] = "%s%s" % (media_url, media_path)
        return ''


def do_device_media_url(parser, token):
    """
    Return a absolute URL for media file in a aware device context.
    If device media URL not exists for that device, MEDIA_URL is inserted.

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


###########
# Filters #
###########

def belongs_to(device, family):
    if callable(getattr(device, 'belongs_to', None)):
        return device.belongs_to(family)
    else:
        return False

register.filter('belongs_to', belongs_to)
