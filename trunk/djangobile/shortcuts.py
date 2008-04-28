# -*- coding: utf-8 -*-
from django.template import loader
from django.http import HttpResponse


def render_to_response(*args, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    content = render_to_ideal(*args, **kwargs)
    return HttpResponse(content, **httpresponse_kwargs)

def render_to_ideal(template_name, dictionary=None, context_instance=None):
    dictionary = dictionary or {}

    if isinstance(template_name, (list, tuple)):
        for template_name in template_name_list:
            try:
                source, origin = loader.find_template_source(template_name)
            except TemplateDoesNotExist:
                raise TemplateDoesNotExist, ', '.join(template_name_list)
    else:
        source, origin = loader.find_template_source(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)

    ideal = IDEAL(source)
    ideal_source = ideal.render(context_instance)
    template = loader.get_template_from_string(ideal_source, origin, template_name)
    return template.render(context_instance)


class IDEAL(object):
    def __init__(self, source, origin=None, name=None):
        self.source = source

    def render(self, context):
        print context
        return self.source
