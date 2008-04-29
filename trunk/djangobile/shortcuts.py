# -*- coding: utf-8 -*-
from os import path

from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from djangobile.template import loader
from djangobile.utils import get_fall_back


def render_to_response(*args, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    content = render_to_ideal(*args, **kwargs)
    return HttpResponse(content, **httpresponse_kwargs)

def render_to_ideal(template_name, dictionary=None, context_instance=None):
    dictionary = dictionary or {}
    user_agent = context_instance.get('HTTP_USER_AGENT', None)
    fall_back = get_fall_back(user_agent)

    if isinstance(template_name, (list, tuple)):
        t = loader.select_template(template_name, fall_back)
    else:
        t = loader.get_template(template_name, fall_back)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    return t.render(context_instance)
