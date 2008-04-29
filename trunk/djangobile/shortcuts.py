# -*- coding: utf-8 -*-
from os import path

from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from djangobile.template import loader
from djangobile.utils import get_device_family


def render_to_response(*args, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    content = render_to_ideal(*args, **kwargs)
    return HttpResponse(content, **httpresponse_kwargs)

def render_to_ideal(template_name, dictionary=None, context_instance=None):
    dictionary = dictionary or {}
    user_agent = context_instance.get('HTTP_USER_AGENT', None)
    device_family = get_device_family(user_agent)

    if isinstance(template_name, (list, tuple)):
        t = loader.select_template(template_name, device_family)
    else:
        t = loader.get_template(template_name, device_family)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    return t.render(context_instance)
