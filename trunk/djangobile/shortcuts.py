# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from djangobile.template import loader


def render_to_response(*args, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    content = render_to_ideal(*args, **kwargs)
    return HttpResponse(content, **httpresponse_kwargs)

def render_to_ideal(template_name, dictionary=None, context_instance=None):
    dictionary = dictionary or {}
    device = context_instance.get('device', None)
    if isinstance(template_name, (list, tuple)):
        t = loader.select_template(template_name, device)
    else:
        t = loader.get_template(template_name, device)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    return t.render(context_instance)
