# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from djangobile.template.loader import render_to_string


def render_to_response(*args, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    content = render_to_string(*args, **kwargs)
    return HttpResponse(content, **httpresponse_kwargs)
